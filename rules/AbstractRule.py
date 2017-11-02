# coding: utf-8

class AbstractRule:
    def __init__(self):
        self._grammar = {}

    def _set_grammar(self, gram):
        # Globalement
        for key, rule in gram.items():
            if gram[key]._calc_valuation() != "je sais pas quoi":
                raise 'Grammaire Incorrecte'  # IncorrectGrammar()
            gram[key] = generate(gram[key])
            # Génere la grammaire en question, soit la succession d'étape pour que
            # self._grammar[key] = Bintree/Fib/Dyck  etc en fonction de la règle
        self._grammar = gram.copy()





if __name__ == '__main__':
    g = AbstractRule({})
