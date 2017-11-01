# coding: utf-8
from rules import ConstructorRule


class UnionRule(ConstructorRule):
    def __init__(self, fst, snd):
        self.fst = fst
        self.snd = snd

    def _calc_valuation(self):
        min(fst.valuation(),snd.valuation())



if __name__ == '__main__':
    pass
