# coding: utf-8
from IPython.lib.editorhooks import kate

from rules.AbstractRule import AbstractRule
from rules.ConstructorRule import ConstructorRule
from rules.ConstanteRule import ConstanteRule
from rules.EpsilonRule import EpsilonRule
from rules.SingletonRule import SingletonRule
from rules.ProductRule import ProductRule
from rules.UnionRule import UnionRule

from Tree import *


treeGram = {"Tree" : UnionRule("Node", "Leaf"),
     "Node" : ProductRule("Tree", "Tree", lambda a, b : Node(a, b)),
     "Leaf" : SingletonRule(Leaf)}

def init_grammar(gram) :
    # absRule = AbstractRule(gram)   tmarti2
    # absRule._set_grammar()         tmarti2

    # Globalement
    for key, rule in gram.items():
        if gram[key]._calc_valuation() != "je sais pas quoi":
            raise 'Grammaire Incorrecte'            #  IncorrectGrammar()
        gram[key] = gram[key]._set_grammar()


# Exemple ici on déclare la grammaire
fiboGram = {"Fib": UnionRule("Vide", "Cas1"),
            "Cas1": UnionRule("CasAu", "Cas2"),
            "Cas2": UnionRule("AtomB", "CasBAu"),
            "Vide": EpsilonRule(""),
            "CasAu": ProductRule("AtomA", "Fib", "".join),
            "AtomA": SingletonRule("A"),
            "AtomB": SingletonRule("B"),
            "CasBAu": ProductRule("AtomB", "CasAu", "".join)}

# pas encore fonctionnelle
# init_grammar(fiboGram)
# fiboGram['Fib'].count(3)







# Puis on l'init mais c'est un effet de bord car après
# ils appellent la grammaire:
# fiboGram['Fib'].count(3)
# sans avoir fait:
# fiboGram['Fib'] = init_grammar(fiboGram)


# Donc init_grammar(fiboGram)
#     Ne renvoit pas un nouvel objet de type AbstractRule.
#     mais plutot fait pour chaque key de fiboGram par exemple:
#     for key, rule in fiboGram:
#         fiboGram[k] = fiboGram[k]._set_grammar()



