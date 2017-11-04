import math
from rules.ConstructorRule import ConstructorRule
from rules.ProductRule import ProductRule
from rules.UnionRule import UnionRule
from rules.ConstanteRule import *
from Tree import *
import unittest


class Main(unittest.TestCase):

    def setUp(self):

        # Exemple ici on déclare la grammaire Tree
        treeGram = {"Tree": UnionRule("Node", "Leaf"),
                    "Node": ProductRule("Tree", "Tree", lambda obj: Node(obj[0], obj[1])),
                    "Leaf": SingletonRule(Leaf)}

        # Exemple ici on déclare la grammaire Fibonacci
        fiboGram = {"Fib": UnionRule("Vide", "Cas1"),
                    "Cas1": UnionRule("CasAu", "Cas2"),
                    "Cas2": UnionRule("AtomB", "CasBAu"),
                    "Vide": EpsilonRule(""),
                    "CasAu": ProductRule("AtomA", "Fib", "".join),
                    "AtomA": SingletonRule("A"),
                    "AtomB": SingletonRule("B"),
                    "CasBAu": ProductRule("AtomB", "CasAu", "".join)}

        # Quesiont 2.2.2
        abWordGram = {"ABWord": UnionRule("Vide", "StartAB"),
                      "StartAB": UnionRule("CasA", "CasB"),
                      "CasA": ProductRule("AtomA", "ABWord", "".join),
                      "CasB": ProductRule("AtomB", "ABWord", "".join),
                      "Vide": EpsilonRule(""),
                      "AtomA": SingletonRule("A"),
                      "AtomB": SingletonRule("B")}
        # Quesiont 2.2.3
        dyckGram = {"DyckWord": UnionRule("Vide", "CasStart"),
                    "CasStart": ProductRule("AtomL", "CasMid", "".join),
                    "CasMid": ProductRule("DyckWord", "CasEnd", "".join),
                    "CasEnd": ProductRule("AtomR", "DyckWord", "".join),
                    "Vide": EpsilonRule(""),
                    "AtomL": SingletonRule("("),
                    "AtomR": SingletonRule(")")}

        # Quesiont 2.2.4
        ab2MaxGram = {"AB2Max": UnionRule("Vide", "Start"),
                      "Start": UnionRule("CasA", "CasB"),
                      "CasA": ProductRule("AtomA", "StartedA", "".join),
                      "CasB": ProductRule("AtomB", "StartedB", "".join),
                      "StartedA": UnionRule("Vide", "NextA"),
                      "StartedB": UnionRule("Vide", "NextB"),
                      "NextA": UnionRule("CasB", "EndA"),
                      "NextB": UnionRule("CasA", "EndB"),
                      "FollowedByA": UnionRule("CasA", "Vide"),
                      "FollowedByB": UnionRule("CasB", "Vide"),
                      "EndA": ProductRule("AtomA", "FollowedByB", "".join),
                      "EndB": ProductRule("AtomB", "FollowedByA", "".join),
                      "Vide": EpsilonRule(""),
                      "AtomA": SingletonRule("A"),
                      "AtomB": SingletonRule("B")}

        # Quesiont 2.2.5.1
        palABGram = {"PalAB": UnionRule("Vide", "StartAB"),
                     "StartAB": UnionRule("CasA", "CasB"),
                     "CasA": ProductRule("AtomA", "EndA", "".join),
                     "CasB": ProductRule("AtomB", "EndB", "".join),
                     "EndA": ProductRule("PalAB", "AtomA", "".join),
                     "EndB": ProductRule("PalAB", "AtomB", "".join),
                     "Vide": EpsilonRule(""),
                     "AtomA": SingletonRule("A"),
                     "AtomB": SingletonRule("B")}

        # Quesiont 2.2.5.2
        palABCGram = {"PalABC": UnionRule("Vide", "StartABC"),
                      "StartABC": UnionRule("CasA", "CasAutre"),
                      "CasAutre": UnionRule("CasB", "CasC"),
                      "CasA": ProductRule("AtomA", "EndA", "".join),
                      "CasB": ProductRule("AtomB", "EndB", "".join),
                      "CasC": ProductRule("AtomC", "EndC", "".join),
                      "EndA": ProductRule("PalABC", "AtomA", "".join),
                      "EndB": ProductRule("PalABC", "AtomB", "".join),
                      "EndC": ProductRule("PalABC", "AtomC", "".join),
                      "Vide": EpsilonRule(""),
                      "AtomA": SingletonRule("A"),
                      "AtomB": SingletonRule("B"),
                      "AtomC": SingletonRule("C")}

        # Quesiont 2.2.6
        autantABGram = {"AutantAB": UnionRule("Vide", "StartAB"),
                        "StartAB": UnionRule("StartWithA", "StartWithB"),
                        "StartWithA": ProductRule("AtomA", "B", "".join),
                        "StartWithB": ProductRule("AtomB", "A", "".join),
                        "A": UnionRule("A2", "BDoubleA"),
                        "A2": ProductRule("AtomA", "AutantAB", "".join),
                        "B": UnionRule("B2", "ADoubleB"),
                        "B2": ProductRule("AtomB", "AutantAB", "".join),
                        "BDoubleA": ProductRule("AtomB", "DoubleA", "".join),
                        "ADoubleB": ProductRule("AtomA", "DoubleB", "".join),
                        "DoubleA": ProductRule("A", "A", "".join),
                        "DoubleB": ProductRule("B", "B", "".join),
                        "Vide": EpsilonRule(""),
                        "AtomA": SingletonRule("A"),
                        "AtomB": SingletonRule("B")}

        self.grammar_list = [treeGram, fiboGram, abWordGram,
                             dyckGram, ab2MaxGram, palABGram,
                             palABCGram, autantABGram]


    def test_Correct_Grammar(self):
        """
        Cas de test que les grammaires soientt correctes c'est a dire :
            - Pour toutes règles: Rule :: UnionRule(A, B) -> A et B != Rule
            - Pour toutes règles: Rule :: Singleton(X) -> Class(X) != AbstractRules
        :return:
        """
        for G in self.grammar_list:
            for sym, r in G.items():
                self.assertTrue(isinstance(sym, str))
                if isinstance(r, UnionRule or ProductRule):
                    self.assertTrue(isinstance(r._parameters[0], str))
                    self.assertTrue(isinstance(r._parameters[1], str))
                    self.assertTrue(sym != r._parameters[0] and sym != r._parameters[1])
                if isinstance(r, ConstanteRule) or issubclass(type(r), ConstanteRule):
                    self.assertTrue(not issubclass(type(r._object), AbstractRule))




if __name__ == '__main__':
    print(__name__)
    unittest.main()