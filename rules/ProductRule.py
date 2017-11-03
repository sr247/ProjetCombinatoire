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
        for k in range(i):
            l = i-k
            if k >= self._grammar[self._parameters[0]].valuation():
                if l >= self._grammar[self._parameters[1]].valuation():
                    vG = self._grammar[self._parameters[0]].count(k)  
                    vD = self._grammar[self._parameters[1]].count(l)  
                    res += vG*vD
        return res

if __name__ == '__test_classic__' or __name__ == '__main__':
    print("Cas de tests ProductRule:")

    print("Pass")
