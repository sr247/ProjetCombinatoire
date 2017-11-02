# coding: utf-8
from rules.ConstructorRule import ConstructorRule


class ProductRule(ConstructorRule):
    def __init__(self, fst, snd, cons):
        super().__init__((fst,snd))
        self._constructor = cons

    def _calc_valuation(self):
        self._parameters[0].valuation()+self._parameters[1].valuation()


if __name__ == '__main__':
    pass
