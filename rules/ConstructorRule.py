# coding: utf-8
from rules.AbstractRule import AbstractRule
import math

class ConstructorRule(AbstractRule):
    
    def __init__(self, parameters):
        self._parameters = parameters
        self._valuation = math.inf

    def valuation(self):
        return self._valuation

    def _update_valuation(self):
        self._valuation = self._calc_valuation()

if __name__ == '__main__':
    pass

