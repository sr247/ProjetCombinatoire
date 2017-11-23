# coding: utf-8
import os
class AbstractRule(object):
    def __init__(self):
        self._grammar = {}

    def _set_grammar(self, gram):
        self._grammar = gram



if __name__ == '__main__':
    print("Cas de tests AbstractRule:")

    # Si un objet AbsRule est crée alors in contient un dictionnaire vide
    Rule = AbstractRule()
    assert (Rule._grammar == {})

    # Si un AbsRule ._set_grammar( G ) alors G et ._grammar ont les memes valeurs
    a = object()
    Rule._set_grammar({"Key": a})
    assert (Rule._grammar == {"Key": a})

    # La grammaire G et la grammaire Rule._grammar sont un meme objet
    G = {'A' : 0, 'B' : 1}
    Rule._set_grammar(G)
    Rule._grammar['A'] = 1
    Rule._grammar['B'] = 0
    assert (Rule._grammar == G == {'A' : 1, 'B' : 0})

    print("Pass")
