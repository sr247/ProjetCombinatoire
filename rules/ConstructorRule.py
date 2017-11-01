# coding: utf-8
from rules import AbstractRule


class ConstructorRule(AbstractRule):
    def __init__(self, parameters, valuation):
        self._parameters = parameters
        self._valuation = valuation

    def valuation(self):
        pass

    def _update_valuation(self):
        pass

if __name__ == '__main__':
    pass