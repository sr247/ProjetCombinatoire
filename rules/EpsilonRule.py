# coding: utf-8
from rules.ConstanteRule import ConstanteRule


class EpsilonRule(ConstanteRule):
    def __init__(self, object):
        self._object = object

    def valuation(self):
        return 0

if __name__ == '__main__':
    pass
