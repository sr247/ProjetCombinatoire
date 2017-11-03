# coding: utf-8
from rules.ConstructorRule import ConstructorRule


class ProductRule(ConstructorRule):
    def __init__(self, fst, snd, cons):
        super().__init__((fst,snd))
        self._constructor = cons


    def _calc_valuation(self):
        valGauche = self._grammar[self._parameters[0]].valuation()
        valDroite = self._grammar[self._parameters[1]].valuation()
        return valGauche+valDroite

    def count(self,i):
        res = 0
        for k in range(i+1):
            l = i-k
            if k >= self._grammar[self._parameters[0]].valuation():
                if l >= self._grammar[self._parameters[1]].valuation():
                    cG = self._grammar[self._parameters[0]].count(k)  
                    cD = self._grammar[self._parameters[1]].count(l)  
                    res += cG*cD
        return res

    def list(self,i):
        res = []
        for k in range(i+1):
            l = i-k
            if k >= self._grammar[self._parameters[0]].valuation():
                if l >= self._grammar[self._parameters[1]].valuation():
                    lG = self._grammar[self._parameters[0]].list(k)  
                    lD = self._grammar[self._parameters[1]].list(l)  
                    for g in lG:
                        for d in lD:
                            res.append(self._constructor((g,d)))
        return res

    def unrank(self,n,r):        
        c = self.count(n)        
        if r >= c:
            raise ValueError("Le rang r (%d) doit etre strictement inférieur au nombre d'objets de taille %d (%d)"%(r,n,c))
        
        acc = 0
        i = -1   
        j = -1   
        for k in range(n+1):
            l = n-k
            if k >= self._grammar[self._parameters[0]].valuation():
                if l >= self._grammar[self._parameters[1]].valuation():
                    cG = self._grammar[self._parameters[0]].count(k)  
                    cD = self._grammar[self._parameters[1]].count(l)  
                    acc += cG*cD
            if r < acc:
                i = k
                acc -= cG*cD
                j = r - acc 
                break

        if i == -1:
            raise Exception("Bad thing happenned")

        k = self._grammar[self._parameters[0]].count(i)  

        q,r = j//k, j%k

        mG = self._grammar[self._parameters[0]].unrank(i,r)
        mD = self._grammar[self._parameters[1]].unrank(n-i,q)  

        return self._constructor((mG,mD))
        
        
        


if __name__ == '__test_classic__' or __name__ == '__main__':
    print("Cas de tests ProductRule:")

    print("Pass")

