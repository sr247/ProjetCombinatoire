# coding: utf-8
from rules.ConstructorRule import ConstructorRule
from Tree import Node
from functools import lru_cache

class UnionRule(ConstructorRule):
    def __init__(self, fst, snd, isFst = None, size = None):
        super().__init__((fst, snd))
        self.isFst = isFst
        self.size = size       
    
    def __repr__(self):
        return "UnionRule("+str(self.parameters[0])+", "+ str(self.parameters[1]) +")"
    
    def __str__(self):
        return "UnionRule("+str(self.parameters[0])+", "+ str(self.parameters[1]) +")"

    def _calc_valuation(self):
        valGauche = self._grammar[self._parameters[0]].valuation()
        valDroite = self._grammar[self._parameters[1]].valuation()
        return min(valGauche, valDroite)

    @lru_cache(maxsize=32)
    def count(self,i):
        countG = self._grammar[self._parameters[0]].count(i)
        countD = self._grammar[self._parameters[1]].count(i)
        return countG + countD

    @lru_cache(maxsize=32)
    def list(self,i):
        listG = self._grammar[self._parameters[0]].list(i)
        listD = self._grammar[self._parameters[1]].list(i)
        return listG + listD

    @lru_cache(maxsize=32)
    def unrank(self, n, r):
        c = self.count(n)
        if r >= c:
            raise ValueError("Le rang r (%d) doit etre strictement inférieur au nombre d'objets de taille %d (%d)"%(r,n,c))

        countG = self._grammar[self._parameters[0]].count(n)
        countD = self._grammar[self._parameters[1]].count(n)
        if r < countG:
            return self._grammar[self._parameters[0]].unrank(n, r)
        else:
            return self._grammar[self._parameters[1]].unrank(n, r-countG)
    
    def rank(self, obj):
        if self.isFst is None or self.size is None :
            raise Exception("Rank n'est pas autorisé sur cette grammaire")
        if self.isFst(obj):
            return self._grammar[self._parameters[0]].rank(obj)
        else: 
            return self._grammar[self._parameters[0]].count(self.size(obj)) + self._grammar[self._parameters[1]].rank(obj)  


class Union():
    def __init__(self,fst,snd):
        self.union = (fst,snd)
    
    def __repr__(self):
        return "Union("+str(self.union[0])+", "+ str(self.union[1]) +")"
    
    def __str__(self):
        return "Union("+str(self.union[0])+", "+ str(self.union[1]) +")"

    def conv(self,gram, key = None):
        fst,snd = self.union
        k1 = fst.conv(gram)
        k2 = snd.conv(gram)
        key = key or "Union-"+str(len(gram))
        gram[key] = UnionRule(k1,k2)
        return key


if __name__ == '__test_classic__' or __name__ == '__main__':
    print("Cas de tests UnionRule:")

    print("Pass")
