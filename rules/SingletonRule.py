# coding: utf-8
from rules import ConstanteRule


class SingletonRule(ConstanteRule):
        def __init__(self, object):
            self._object = object


if __name__ == '__main__':
    pass