# coding: utf-8
from rules import ConstructorRule


class ProductRule(ConstructorRule):
    def __init__(self, fst, snd, cons):
        self._constructor = cons

    def _calc_valuation(self):
        pass


if __name__ == '__main__':
    pass