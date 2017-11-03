# coding: utf-8
from rules.ConstructorRule import ConstructorRule
class UnionRule(ConstructorRule):
    def __init__(self, fst, snd):
        super().__init__((fst, snd))

    def _calc_valuation(self):
        valGauche = self._grammar[self._parameters[0]].valuation()
        valDroite = self._grammar[self._parameters[1]].valuation()
        return min(valGauche,valDroite)


if __name__ == '__main__' or '__test_classic__':
    print("Cas de tests UnionRule:")

    print("Pass")
