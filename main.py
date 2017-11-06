# coding: utf-8
import math
import time
from profile import Profile

from rules.ConstructorRule import *
from rules.ProductRule import *
from rules.UnionRule import *
from rules.ConstanteRule import *
from Tree import *

class Bound():
    def __init__(self,C,min,max):
        self._list = []
        self._count = []
        for i in range(min,max+1):
            self._list += C.list(i)
            self._count.append(C.count(i))
            
            
def convGramCond(gram,key):
    gram[key].conv(gram,key)


def init_grammar(gram):
    """
    Fonction d'initialisation de la grammaire
    :param gram: La grammaire à générer
    :return: None
    """
    for key in gram.keys() :
        gram[key]._set_grammar(gram)
    
    for key in gram.keys() :
        if not gram[key].check(key):
          raise Exception("Grammaire Incorrecte : Nonterm %s inconnue ou Recursion infini sur le non-terminal "%key +key)
    
    # Booléen qui indique si le point fix est trouvé ou non (vrai = non trouvé, false = trouvé)
    not_found = True

    # Tant qu'on a pas trouvé le point fix
    while not_found:
        not_found = False
        # Pour toutes les règles héritant de ConstructorRule
        for key in [ x for x in gram.keys() if isinstance(gram[x],ConstructorRule)] :
            # On stock la valuation précédentte (Vn-1)
            vpre = gram[key].valuation()
            # On calcule la valuation courante (Vn)
            gram[key]._update_valuation()
            vcur = gram[key].valuation()
            # Si les 2 valeurs sont différentes ou que la valuation à renvoyé l'infini
            if (vpre != vcur):
                # Alors on a pas encore trouvé le point fix
                not_found = True

    for key in gram.keys() :
        if gram[key].valuation() == math.inf:
            raise Exception("Grammaire Incorrecte : Valuation infini")


if __name__ == '__main__':
    
    # Exemple ici on déclare la grammaire Tree
    size = lambda tree : tree.size()
    isFst = lambda tree : not tree.is_leaf()
    pack = lambda obj: Node(obj[0], obj[1])
    unpack = lambda tree : (tree.left(),tree.right())

    treeGram = {"Tree": UnionRule("Node", "Leaf", isFst, size),
                "Node": ProductRule("Tree", "Tree", pack, unpack, size),
                "Leaf": SingletonRule(Leaf)}

    treeGramCond = {"Tree" : Union(Prod(NonTerm("Tree"), NonTerm("Tree"), pack, unpack, size), Singleton(Leaf), isFst,size)}
    convGramCond(treeGramCond,"Tree")

     

    unpack = lambda s : (s[:1],s[1:])
    isFstA = lambda s : s[:1] == 'A'
    size = lambda s : len(s)
    isEmpty = lambda s : s==""
    
    treeGramCond2 = {"Flower" : Union(Prod(Singleton("o"), NonTerm("Flower"), pack, unpack, size), Singleton("o"), isFst,size)}
    convGramCond(treeGramCond2,"Flower")

    print(treeGramCond2)
    
    #Sequence
    testSequence = {"SeqA" : Sequence("AtomA", "", "".join, unpack, isEmpty, size),
         "AtomA": SingletonRule("a")}
         
    convGramCond(testSequence,"SeqA")
         


    # ces fonctions sont utilisées dans la plus part des cas sur les grammaires fonctionnant avec des objets de type string
    size = lambda s : len(s)
    isEmpty = lambda s : s==""
    unpack = lambda s : (s[:1],s[1:]) #Premier caractère et le reste
    unpack2 = lambda s : (s[:len(s)-1],s[len(s)-1]) #Tout sauf le dernier caractère et le dernier caractère
    isFstA = lambda s : s[:1] == 'A'
    isFstB = lambda s : s[:1] == 'B'
    single = lambda s : len(s) == 1
    join = "".join

    # Exemple ici on déclare la grammaire Fibonacci
    isFstB1 = lambda s : len(s) == 1 and s[:1] == 'B'
    fiboGram = {"Fib": UnionRule("Vide", "Cas1", isEmpty, size),
                "Cas1": UnionRule("CasAu", "Cas2", isFstA, size),
                "Cas2": UnionRule("AtomB", "CasBAu",isFstB1, size),
                "CasAu": ProductRule("AtomA", "Fib", join, unpack, size),
                "CasBAu": ProductRule("AtomB", "CasAu", join, unpack, size),
                "Vide": EpsilonRule(""),
                "AtomA": SingletonRule("A"),
                "AtomB": SingletonRule("B")}
    
    
    #Quesiont 2.2.2
    abWordGram = {"ABWord": UnionRule("Vide", "StartAB", isEmpty, size),
                  "StartAB": UnionRule("CasA", "CasB", isFstA, size),
                  "CasA": ProductRule("AtomA","ABWord", join, unpack, size),
                  "CasB": ProductRule("AtomB","ABWord", join, unpack, size),
                  "Vide": EpsilonRule(""),
                  "AtomA": SingletonRule("A"),
                  "AtomB": SingletonRule("B")}

    
    #Quesiont 2.2.3
    dyckGram = {"DyckWord" : UnionRule("Vide","CasStart",isEmpty,size),
                "CasStart": ProductRule("AtomL","CasMid", join, unpack, size),
                "CasMid": ProductRule("DyckWord","CasEnd", join, unpack2, size),
                "CasEnd": ProductRule("AtomR","DyckWord", join, unpack, size),
                "Vide": EpsilonRule(""),
                "AtomL": SingletonRule("("),
                "AtomR": SingletonRule(")")}

    #Quesiont 2.2.4	
    ab2MaxGram = {"AB2Max": UnionRule("Vide","Start",isEmpty,size),
                  "Start": UnionRule("CasA","CasB",isFstA,size),
                  "CasA": ProductRule("AtomA","StartedA", join, unpack, size),
                  "CasB": ProductRule("AtomB","StartedB", join, unpack, size),
                  "StartedA": UnionRule("Vide","NextA",isEmpty,size),
                  "StartedB": UnionRule("Vide","NextB",isEmpty,size),
                  "NextA": UnionRule("CasB","EndA", isFstB, size),
                  "NextB": UnionRule("CasA","EndB", isFstA, size),
                  "FollowedByA": UnionRule("CasA","Vide", isFstA, size),
                  "FollowedByB": UnionRule("CasB","Vide", isFstB, size),
                  "EndA": ProductRule("AtomA","FollowedByB", join, unpack, size),
                  "EndB": ProductRule("AtomB","FollowedByA", join, unpack, size),
                  "Vide": EpsilonRule(""),
                  "AtomA": SingletonRule("A"),
                  "AtomB": SingletonRule("B")}

    #Quesiont 2.2.5.1
    palABGram = {"PalAB": UnionRule("Vide","StartAB", isEmpty, size),
                 "StartAB": UnionRule("Single","Sym", single, size),
                 "Single": UnionRule("AtomA","AtomB", isFstA, size),
                 "Sym": UnionRule("SymA","SymB", isFstA, size),
                 "SymA": ProductRule("AtomA","SymA2", join, unpack, size),
                 "SymB": ProductRule("AtomB","SymB2", join, unpack, size),
                 "SymA2": ProductRule("PalAB","AtomA", join, unpack2, size),
                 "SymB2": ProductRule("PalAB","AtomB", join, unpack2, size),
                 "Vide": EpsilonRule(""),
                 "AtomA": SingletonRule("A"),
                 "AtomB": SingletonRule("B")}
    
    #Quesiont 2.2.5.1
    palABCGram = {"PalABC": UnionRule("Vide","StartABC", isEmpty, size),
                 "StartABC": UnionRule("Single","Sym", single, size),
                 "Single": UnionRule("AtomA","Single2", isFstA, size),
                 "Single2": UnionRule("AtomB","AtomC", isFstB, size),
                 "Sym": UnionRule("SymA","Sym2", isFstA, size),
                 "Sym2": UnionRule("SymB","SymC", isFstB, size),
                 "SymA": ProductRule("AtomA","SymA2", join, unpack, size),
                 "SymB": ProductRule("AtomB","SymB2", join, unpack, size),
                 "SymC": ProductRule("AtomC","SymC2", join, unpack, size),
                 "SymA2": ProductRule("PalABC","AtomA", join, unpack2, size),
                 "SymB2": ProductRule("PalABC","AtomB", join, unpack2, size),
                 "SymC2": ProductRule("PalABC","AtomC", join, unpack2, size),
                 "Vide": EpsilonRule(""),
                 "AtomA": SingletonRule("A"),
                 "AtomB": SingletonRule("B"),
                 "AtomC": SingletonRule("C")}

    #Quesiont 2.2.6
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
    
    name = ["SeqA","Tree","Tree", "Fib", "ABWord", "DyckWord", "AB2Max", "PalAB", "PalABC", "AutantAB"]

    print("")

    tGram = [testSequence,treeGram,treeGramCond, fiboGram, abWordGram, dyckGram, ab2MaxGram, palABGram, palABCGram, autantABGram]

    print(tGram[0])
    
    
    for g in tGram:
        init_grammar(g)
    
    print(tGram[0]['SeqA'].list(6))
    
    print(tGram[0]['SeqA'].unrank(20,0))
    
    
    for i in range(len(tGram)):
        g = tGram[i][name[i]]
        for n in range(0,12):
  
            l1 = g.list(n)
            l2 = [g.unrank(n, v) for v in range(len(l1))]

            for i in range(len(l1)):
                assert(l1[i] == l2[i])
        print("Pass")
        
    #b = Bound(test['Tree'],0,4)
    #for el in b._list:
    #    print(el)

    #start = time.time()
    #print(tGram[0]['Tree'].count(13))
    #end = time.time()
    #print(end-start)

    # Affiche les valeurs des valuations de tGram[i]
    # for key in tGram[1].keys():
    #     print(key, ":", tGram[1][key].valuation())


