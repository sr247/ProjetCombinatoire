# coding: utf-8
from rules.AbstractRule import AbstractRule

class ConstructorRule(AbstractRule):
    
    def __init__(self, parameters):
        self._parameters = parameters
        self._valuation = 0

    def valuation(self):
        self._calc_valuation()

    def _update_valuation(self):
        self._valuation = self.valuation()

if __name__ == '__main__':
    pass
