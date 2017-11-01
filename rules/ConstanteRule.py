# coding: utf-8
from rules import AbstractRule

class ConstanteRule(AbstractRule):
    def __init__(self,object):
        self._object = object

    def valuation(self):
        if isinstance(self,EpsilonRule):
            return 0
        else:
            return 1

if __name__ == '__main__':
    pass
