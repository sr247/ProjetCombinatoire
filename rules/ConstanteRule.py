# coding: utf-8
from rules.AbstractRule import AbstractRule

class ConstanteRule(AbstractRule):
    def __init__(self, object):
        self._object = object

    # Ici Epsilon Rules n'est pas connu...
    # Possiblement ça peut exploser
    def valuation(self):
        print(self._object)

if __name__ == '__main__':
    pass
