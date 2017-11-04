# coding: utf-8
from rules.ConstructorRule import ConstructorRule
from Tree import Node


class UnionRule(ConstructorRule):
    def __init__(self, fst, snd, leftOrRight = None, size = None):
        super().__init__((fst, snd))
        self.leftOrRight = leftOrRight
        self.size = size       

    def _calc_valuation(self):
        valGauche = self._grammar[self._parameters[0]].valuation()
        valDroite = self._grammar[self._parameters[1]].valuation()
        return min(valGauche, valDroite)

    def count(self,i):
        countG = self._grammar[self._parameters[0]].count(i)
        countD = self._grammar[self._parameters[1]].count(i)
        return countG + countD

    def list(self,i):
        listG = self._grammar[self._parameters[0]].list(i)
        listD = self._grammar[self._parameters[1]].list(i)
        return listG + listD

    def unrank(self, n, r):
        c = self.count(n)
        if r >= c:
            raise ValueError("Le rang r (%d) doit etre strictement inférieur au nombre d'objets de taille %d (%d)"%(r,i,c))

        countG = self._grammar[self._parameters[0]].count(n)
        countD = self._grammar[self._parameters[1]].count(n)
        if r < countG:
            return self._grammar[self._parameters[0]].unrank(n, r)
        else:
            return self._grammar[self._parameters[1]].unrank(n, r-countG)

    def rank(self, obj):
        if self.leftOrRight is None or self.size is None :
            raise Exception("Rank n'est pas autorisé sur cette grammaire")
        if  self.leftOrRight(obj):  
            return self._grammar[self._parameters[0]].count(self.size(obj)) + self._grammar[self._parameters[1]].rank(obj)
        else:
            return self._grammar[self._parameters[0]].rank(obj)   


if __name__ == '__test_classic__' or __name__ == '__main__':
    print("Cas de tests UnionRule:")

    print("Pass")
