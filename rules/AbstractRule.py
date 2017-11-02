# coding: utf-8

class AbstractRule:
    def __init__(self, gram):
        self._grammar = gram

    def _set_grammar(self):
        # Globalement
        for key, rule in self._grammar.items():
            if self._grammar[key]._calc_valuation() != "je sais pas quoi":
                raise 'Grammaire Incorrecte'  # IncorrectGrammar()
            self._grammar[key] = self._grammar[key]._set_grammar()

if __name__ == '__main__':
    pass
