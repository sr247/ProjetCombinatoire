# coding: utf-8
from rules.ConstructorRule import ConstructorRule
class UnionRule(ConstructorRule):
    def __init__(self, fst, snd):
        super().__init__((fst, snd))

    def _calc_valuation(self):
        valGauche = self._grammar[self._parameters[0]].valuation()
        valDroite = self._grammar[self._parameters[1]].valuation()
        return min(valGauche,valDroite)

    def count(self,i):
        countG = self._grammar[self._parameters[0]].count(i)
        countD = self._grammar[self._parameters[1]].count(i)
        return countG + countD

    def list(self,i):
        listG = self._grammar[self._parameters[0]].list(i)
        listD = self._grammar[self._parameters[1]].list(i)
        return listG + listD

if __name__ == '__test_classic__' or __name__ == '__main__':
    print("Cas de tests UnionRule:")
    print("Pass")
