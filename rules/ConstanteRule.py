# coding: utf-8
from rules.AbstractRule import AbstractRule

class ConstanteRule(AbstractRule):
    def __init__(self, object):
        self._object = object

    # Ici Epsilon Rules n'est pas connu...
    # Possiblement ça peut exploser
    def valuation(self):
        if isinstance(self, EpsilonRule):
            return 0
        else:
            return 1

if __name__ == '__main__':
    pass
