import math
from rules.ConstructorRule import ConstructorRule
from rules.ProductRule import ProductRule
from rules.UnionRule import UnionRule
from rules.ConstanteRule import *
from Tree import *
import unittest
import main

class Main(unittest.TestCase):

    def setUp(self):

        # Exemple ici on déclare la grammaire Tree
        size = lambda tree: tree.size()
        isFst = lambda tree: not tree.is_leaf()
        pack = lambda obj: Node(obj[0], obj[1])
        unpack = lambda tree: (tree.left(), tree.right())

        treeGram = {"Tree": UnionRule("Node", "Leaf", isFst, size),
                    "Node": ProductRule("Tree", "Tree", pack, unpack, size),
                    "Leaf": SingletonRule(Leaf)}

        # ces fonctions sont utilisés dans la plus part des cas sur les grammaires fonctionannt avec des objets de type string
        size = lambda s: len(s)
        isEmpty = lambda s: s == ""
        unpack = lambda s: (s[:1], s[1:])
        unpack2 = lambda s: (s[:len(s) - 1], s[len(s) - 1])
        isFstA = lambda s: s[:1] == 'A'
        isFstB = lambda s: s[:1] == 'B'
        single = lambda s: len(s) == 1
        join = "".join

        # Exemple ici on déclare la grammaire Fibonacci
        isFstB1 = lambda s: len(s) == 1 and s[:1] == 'B'
        fiboGram = {"Fib": UnionRule("Vide", "Cas1", isEmpty, size),
                    "Cas1": UnionRule("CasAu", "Cas2", isFstA, size),
                    "Cas2": UnionRule("AtomB", "CasBAu", isFstB1, size),
                    "CasAu": ProductRule("AtomA", "Fib", join, unpack, size),
                    "CasBAu": ProductRule("AtomB", "CasAu", join, unpack, size),
                    "Vide": EpsilonRule(""),
                    "AtomA": SingletonRule("A"),
                    "AtomB": SingletonRule("B")}

        # Quesiont 2.2.2
        abWordGram = {"ABWord": UnionRule("Vide", "StartAB", isEmpty, size),
                      "StartAB": UnionRule("CasA", "CasB", isFstA, size),
                      "CasA": ProductRule("AtomA", "ABWord", join, unpack, size),
                      "CasB": ProductRule("AtomB", "ABWord", join, unpack, size),
                      "Vide": EpsilonRule(""),
                      "AtomA": SingletonRule("A"),
                      "AtomB": SingletonRule("B")}

        # Quesiont 2.2.3
        dyckGram = {"DyckWord": UnionRule("Vide", "CasStart", isEmpty, size),
                    "CasStart": ProductRule("AtomL", "CasMid", join, unpack, size),
                    "CasMid": ProductRule("DyckWord", "CasEnd", join, unpack2, size),
                    "CasEnd": ProductRule("AtomR", "DyckWord", join, unpack, size),
                    "Vide": EpsilonRule(""),
                    "AtomL": SingletonRule("("),
                    "AtomR": SingletonRule(")")}

        # Quesiont 2.2.4
        ab2MaxGram = {"AB2Max": UnionRule("Vide", "Start", isEmpty, size),
                      "Start": UnionRule("CasA", "CasB", isFstA, size),
                      "CasA": ProductRule("AtomA", "StartedA", join, unpack, size),
                      "CasB": ProductRule("AtomB", "StartedB", join, unpack, size),
                      "StartedA": UnionRule("Vide", "NextA", isEmpty, size),
                      "StartedB": UnionRule("Vide", "NextB", isEmpty, size),
                      "NextA": UnionRule("CasB", "EndA", isFstB, size),
                      "NextB": UnionRule("CasA", "EndB", isFstA, size),
                      "FollowedByA": UnionRule("CasA", "Vide", isFstA, size),
                      "FollowedByB": UnionRule("CasB", "Vide", isFstB, size),
                      "EndA": ProductRule("AtomA", "FollowedByB", join, unpack, size),
                      "EndB": ProductRule("AtomB", "FollowedByA", join, unpack, size),
                      "Vide": EpsilonRule(""),
                      "AtomA": SingletonRule("A"),
                      "AtomB": SingletonRule("B")}

        # Quesiont 2.2.5.1
        palABGram = {"PalAB": UnionRule("Vide", "StartAB", isEmpty, size),
                     "StartAB": UnionRule("Single", "Sym", single, size),
                     "Single": UnionRule("AtomA", "AtomB", isFstA, size),
                     "Sym": UnionRule("SymA", "SymB", isFstA, size),
                     "SymA": ProductRule("AtomA", "SymA2", join, unpack, size),
                     "SymB": ProductRule("AtomB", "SymB2", join, unpack, size),
                     "SymA2": ProductRule("PalAB", "AtomA", join, unpack2, size),
                     "SymB2": ProductRule("PalAB", "AtomB", join, unpack2, size),
                     "Vide": EpsilonRule(""),
                     "AtomA": SingletonRule("A"),
                     "AtomB": SingletonRule("B")}

        # Quesiont 2.2.5.1
        palABCGram = {"PalABC": UnionRule("Vide", "StartABC", isEmpty, size),
                      "StartABC": UnionRule("Single", "Sym", single, size),
                      "Single": UnionRule("AtomA", "Single2", isFstA, size),
                      "Single2": UnionRule("AtomB", "AtomC", isFstB, size),
                      "Sym": UnionRule("SymA", "Sym2", isFstA, size),
                      "Sym2": UnionRule("SymB", "SymC", isFstB, size),
                      "SymA": ProductRule("AtomA", "SymA2", join, unpack, size),
                      "SymB": ProductRule("AtomB", "SymB2", join, unpack, size),
                      "SymC": ProductRule("AtomC", "SymC2", join, unpack, size),
                      "SymA2": ProductRule("PalABC", "AtomA", join, unpack2, size),
                      "SymB2": ProductRule("PalABC", "AtomB", join, unpack2, size),
                      "SymC2": ProductRule("PalABC", "AtomC", join, unpack2, size),
                      "Vide": EpsilonRule(""),
                      "AtomA": SingletonRule("A"),
                      "AtomB": SingletonRule("B"),
                      "AtomC": SingletonRule("C")}

        # Quesiont 2.2.6
        # Grammaire ambigue : rank impossible
        autantABGram = {"AutantAB": UnionRule("Vide", "StartAB"),
                        "StartAB": UnionRule("StartWithA", "StartWithB"),
                        "StartWithA": ProductRule("AtomA", "B", join),
                        "StartWithB": ProductRule("AtomB", "A", join),
                        "A": UnionRule("A2", "BDoubleA"),
                        "A2": ProductRule("AtomA", "AutantAB", join),
                        "B": UnionRule("B2", "ADoubleB"),
                        "B2": ProductRule("AtomB", "AutantAB", join),
                        "BDoubleA": ProductRule("AtomB", "DoubleA", join),
                        "ADoubleB": ProductRule("AtomA", "DoubleB", join),
                        "DoubleA": ProductRule("A", "A", join),
                        "DoubleB": ProductRule("B", "B", join),
                        "Vide": EpsilonRule(""),
                        "AtomA": SingletonRule("A"),
                        "AtomB": SingletonRule("B")}

        self.grammar_list = [treeGram, fiboGram, abWordGram,
                             dyckGram, ab2MaxGram, palABGram,
                             palABCGram, autantABGram]
        self.name = ["Tree", "Fib", "ABWord", "DyckWord", "AB2Max", "PalAB", "PalABC", "AutantAB"]

        for g in self.grammar_list:
            main.init_grammar(g)

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
        print("Pass")


    def test_Correct_Count(self):
        j=0
        for i in range(len(self.grammar_list)):
            for k in range(10):
                a = self.grammar_list[i][self.name[j]].count(k)
                b = len(self.grammar_list[i][self.name[j]].list(k))
                self.assertTrue(a == b)
            j += 1


    def test_Correct_Unrank(self):
        j = 0
        for k in range(len(self.grammar_list)):
            for n in range(0,10):

                l1 = self.grammar_list[k][self.name[j]].list(n)
                l2 = [self.grammar_list[k][self.name[j]].unrank(n, v) for v in range(len(l1))]


                for id1 in range(len(l1)):
                    for id2 in range(len(l2)):
                        if l2[id1] == l1[id2] and 18<id1<23 and  18<id2<23:
                            print("unrank(%d %d)"%(n, id1) ,"== list(%d)"%id2)

                for i in range(len(l1)):
                    unranked = self.grammar_list[k][self.name[j]].unrank(n, i)

                    v = 20
                    self.assertTrue(l1[i] == unranked,
                                    msg="\n{} n={} i={}\nlist({})[{}]  {}\nunrank({},{}) {}".format(self.grammar_list[k],n,i,n,i,
                                                                       l1[v],n,i, self.grammar_list[k][self.name[j]].unrank(n, v)))
            j += 1
        print("Pass")

if __name__ == '__main__':

    unittest.main()
