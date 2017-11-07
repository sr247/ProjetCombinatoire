import sys
sys.path.insert(0,'..')

import unittest

from ConstanteRule import *
from ProductRule import *
from UnionRule import *
from main import init_grammar, convGramCond

import main
from Tree import *


class Main(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        # Fonctions principalement utilisées pour les Trees
        size = lambda tree: tree.size()
        isFst = lambda tree: not tree.is_leaf()
        pack = lambda obj: Node(obj[0], obj[1])
        unpack = lambda tree: (tree.left(), tree.right())

        # Ces fonctions sont utilisées dans la plus part des cas sur les grammaires fonctionnant avec des objets de type string
        size = lambda s: len(s)
        isEmpty = lambda s: s == ""
        unpack = lambda s: (s[:1], s[1:])  # Premier caractère et le reste
        unpack2 = lambda s: (s[:len(s) - 1], s[len(s) - 1])  # Tout sauf le dernier caractère et le dernier caractèreisFstA = lambda s: s[:1] == 'A'
        isFstA = lambda s: s[:1] == '1'        
        isFstB = lambda s: s[:1] == 'B'
        single = lambda s: len(s) == 1
        join = "".join

        # Exemple ici on déclare la grammaire Tree
        treeGram = {"Tree": UnionRule("Node", "Leaf", isFst, size),
                    "Node": ProductRule("Tree", "Tree", pack, unpack, size),
                    "Leaf": SingletonRule(Leaf)}

        # Exemple de grammaire condensée + conversion
        treeGramCond = {
            "Tree": Union(Prod(NonTerm("Tree"), NonTerm("Tree"), pack, unpack, size), Singleton(Leaf), isFst, size)}
        convGramCond(treeGramCond, "Tree")

        # Exemple de grammaire condensée avec propagation des clefs sur des valeurs de règles identiques
        treeGramCond2 = {
            "Flower": Union(Prod(Singleton("o"), NonTerm("Flower"), pack, unpack, size), Singleton("o"), isFst, size)}
        convGramCond(treeGramCond2, "Flower")

        # Sequence Simple
        testSequence = {"SeqA": Sequence("AtomA", "", "".join, unpack, isEmpty, size), "AtomA": SingletonRule("a")}
        convGramCond(testSequence, "SeqA")

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


        cls.grammar_list = [testSequence, treeGram, treeGramCond, fiboGram, abWordGram, dyckGram, ab2MaxGram, palABGram,
                 palABCGram, autantABGram]

        cls.name = ["SeqA", "Tree", "Tree", "Fib", "ABWord", "DyckWord", "AB2Max", "PalAB", "PalABC", "AutantAB"]

        for g in cls.grammar_list:
            main.init_grammar(g)

    def setUp(self):
        pass        
        #print("Test", self.

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


    def test_Correct_Count(self):
        j=0
        for i in range(len(self.grammar_list)):
            for k in range(10):
                a = self.grammar_list[i][self.name[j]].count(k)
                b = len(self.grammar_list[i][self.name[j]].list(k))
                self.assertEqual(a, b)
            j += 1


    def test_Correct_Unrank(self):
        j = 0
        for k in range(len(self.grammar_list)):
            for n in range(0,10):

                l1 = self.grammar_list[k][self.name[j]].list(n)
                l2 = [self.grammar_list[k][self.name[j]].unrank(n, v) for v in range(len(l1))]


                # for id1 in range(len(l1)):
                #     for id2 in range(len(l2)):
                #         if l2[id1] == l1[id2]:
                #             print("unrank(%d %d)"%(n, id1) ,"== list(%d)"%id2)

                for i in range(len(l1)):
                    unranked = self.grammar_list[k][self.name[j]].unrank(n, i)

                    self.assertTrue(l1[i] == unranked,
                                    msg="\n{} n={} i={}\nlist({})[{}]  {}\nunrank({},{}) {}".format(self.grammar_list[k],n,i,n,i,
                                                                       l1[i],n,i, self.grammar_list[k][self.name[j]].unrank(n, i)))
            j += 1

    def test_Correct_Tree(self):
        pass


    def test_correct_Fib(self):
        pass


if __name__ == '__main__':

    unittest.main()
