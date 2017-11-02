# coding: utf-8

class AbstractRule:
    def __init__(self):
        self._grammar = {}

    def _set_grammar(self, gram):
        self._grammar = gram

if __name__ == '__main__':
    g = AbstractRule({})
