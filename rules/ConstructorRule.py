# coding: utf-8
from rules import AbstractRule


class ConstructorRule(AbstractRule):
    def __init__(self, parameters):
        self._parameters = parameters
        self._valuation = 0

    def valuation(self):
        pass

    def _update_valuation(self):
        pass

if __name__ == '__main__':
    pass
