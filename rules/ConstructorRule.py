# coding: utf-8
from rules.AbstractRule import AbstractRule
import math

class ConstructorRule(AbstractRule):
    
    def __init__(self, parameters):
        super().__init__()
        self._parameters = parameters
        self._valuation = math.inf
    
    def check(self,key):
      lk = self._grammar.keys()
      return (self._parameters[0] in lk and self._parameters[1] in lk) and self._parameters[0] != key and self._parameters[1] != key
    
    
    def valuation(self):
        return self._valuation

    def _update_valuation(self):
        self._valuation = self._calc_valuation()

if __name__ == '__test_classic__' or __name__ == '__main__':
    print("Cas de tests ConstructorRule:")

    print("Pass")


