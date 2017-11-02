# coding: utf-8
from rules.ConstructorRule import ConstructorRule

class UnionRule(ConstructorRule):
    def __init__(self, fst, snd):
        super().__init__((fst,snd))

    def _calc_valuation(self):
        min(self._parameters[0].valuation(),self._parameters[1].valuation())


if __name__ == '__main__':
    pass
