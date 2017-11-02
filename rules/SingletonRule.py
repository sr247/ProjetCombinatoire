# coding: utf-8
from rules.ConstanteRule import ConstanteRule


class SingletonRule(ConstanteRule):
        def __init__(self, object):
            self._object = object

        def valuation(self):
            return 1


if __name__ == '__main__':
    pass
