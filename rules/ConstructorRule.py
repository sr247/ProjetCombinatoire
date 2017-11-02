# coding: utf-8
from rules.AbstractRule import AbstractRule
import sys


class ConstructorRule(AbstractRule):
    
    def __init__(self, parameters):
        self._parameters = parameters
        self._valuation = sys.maxsize

    def valuation(self):
        return self._valuation

    def _update_valuation(self):
        self._valuation = self._calc_valuation()
            



if __name__ == '__main__':
    pass

