# coding: utf-8
from rules import ConstructorRule


class UnionRule(ConstructorRule):
    def __init__(self, fst, snd):
        self._parameters = (fst,snd)

    def _calc_valuation(self):
        min(_parameters[0].valuation(),_parameters[1].valuation())


if __name__ == '__main__':
    pass
