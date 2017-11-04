# coding: utf-8
import math
from rules.ConstructorRule import ConstructorRule
from rules.ProductRule import ProductRule
from rules.UnionRule import UnionRule
from rules.ConstanteRule import *

from Tree import *

def check_grammar(gram):
    """
    Fonction qui vérifie que la grammaire est bien définie
    :param gram: La grammaire à vérifier
    :return: Exception si gram invalide
    """
    pass

def init_grammar(gram) :
    """
    Fonction d'initialisation de la grammaire
    :param gram: La grammaire à générer
    :return: None
    """
    check_grammar(gram)
    for key in gram.keys() :
        gram[key]._set_grammar(gram)
    
    # Booléen qui indique si le point fix est trouvé ou non (vrai = non trouvé, false = trouvé)
    still = True
    
    n = 100
    cpt = 0

    # Tant qu'on a pas trouvé le point fix
    while still and cpt < n:
        cpt += 1
        still = False
        # Pour toutes les règles héritant de ConstructorRule
        for key in [ x for x in gram.keys() if isinstance(gram[x],ConstructorRule)] :
            # On stock la valuation précédentte (Vn-1)
            vpre = gram[key].valuation()
            # On calcule la valuation courante (Vn)
            gram[key]._update_valuation()
            vcur = gram[key].valuation()
            # Si les 2 valeurs sont différentes ou que la valuation à renvoyé l'infini
            if (vpre != vcur or vcur == math.inf):
                # Alors on a pas encore trouvé le point fix
                still = True
    if cpt == n and still:
        raise Exception("Grammaire Incorrecte : Valuation infini")




if __name__ == '__main__':
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
    
    #Quesiont 2.2.2
    abWordGram = {"ABWord": UnionRule("Vide", "StartAB"),
                  "StartAB": UnionRule("CasA", "CasB"),
                  "CasA": ProductRule("AtomA","ABWord", "".join),
                  "CasB": ProductRule("AtomB","ABWord", "".join),
                  "Vide": EpsilonRule(""),
                  "AtomA": SingletonRule("A"),
                  "AtomB": SingletonRule("B")}
    #Quesiont 2.2.3
    dyckGram = {"DyckWord" : UnionRule("Vide","CasStart"),
                "CasStart": ProductRule("AtomL","CasMid", "".join),
                "CasMid": ProductRule("DyckWord","CasEnd", "".join),
                "CasEnd": ProductRule("AtomR","DyckWord", "".join),
                "Vide": EpsilonRule(""),
                "AtomL": SingletonRule("("),
                "AtomR": SingletonRule(")")}

    #Quesiont 2.2.4	
    ab2MaxGram = {"AB2Max": UnionRule("Vide","Start"),
                  "Start": UnionRule("CasA","CasB"),
                  "CasA": ProductRule("AtomA","StartedA", "".join),
                  "CasB": ProductRule("AtomB","StartedB", "".join),
                  "StartedA": UnionRule("Vide","NextA"),
                  "StartedB": UnionRule("Vide","NextB"),
                  "NextA": UnionRule("CasB","EndA"),
                  "NextB": UnionRule("CasA","EndB"),
                  "FollowedByA": UnionRule("CasA","Vide"),
                  "FollowedByB": UnionRule("CasB","Vide"),
                  "EndA": ProductRule("AtomA","FollowedByB", "".join),
                  "EndB": ProductRule("AtomB","FollowedByA", "".join),
                  "Vide": EpsilonRule(""),
                  "AtomA": SingletonRule("A"),
                  "AtomB": SingletonRule("B")}

    #Quesiont 2.2.5.1
    palABGram = {"PalAB": UnionRule("Vide","StartAB"),
                 "StartAB": UnionRule("Single","Sym"),
                 "Single": UnionRule("AtomA","AtomB"),
                 "Sym": UnionRule("SymA","SymB"),
                 "SymA": ProductRule("AtomA","SymA2", "".join),
                 "SymB": ProductRule("AtomB","SymB2", "".join),
                 "SymA2": ProductRule("PalAB","AtomA", "".join),
                 "SymB2": ProductRule("PalAB","AtomB", "".join),
                 "Vide": EpsilonRule(""),
                 "AtomA": SingletonRule("A"),
                 "AtomB": SingletonRule("B")}
    
    #Quesiont 2.2.5.1
    palABCGram = {"PalABC": UnionRule("Vide","StartABC"),
                 "StartABC": UnionRule("Single","Sym"),
                 "Single": UnionRule("AtomA","Single2"),
                 "Single2": UnionRule("AtomB","AtomC"),
                 "Sym": UnionRule("SymA","Sym2"),
                 "Sym2": UnionRule("SymB","SymC"),
                 "SymA": ProductRule("AtomA","SymA2", "".join),
                 "SymB": ProductRule("AtomB","SymB2", "".join),
                 "SymC": ProductRule("AtomC","SymC2", "".join),
                 "SymA2": ProductRule("PalABC","AtomA", "".join),
                 "SymB2": ProductRule("PalABC","AtomB", "".join),
                 "SymC2": ProductRule("PalABC","AtomC", "".join),
                 "Vide": EpsilonRule(""),
                 "AtomA": SingletonRule("A"),
                 "AtomB": SingletonRule("B"),
                 "AtomC": SingletonRule("C")}

    #Quesiont 2.2.6
    autantABGram = {"AutantAB": UnionRule("Vide","StartAB"),
                    "StartAB": UnionRule("StartWithA","StartWithB"),
                    "StartWithA": ProductRule("AtomA","B", "".join),
                    "StartWithB": ProductRule("AtomB","A", "".join),
                    "A": UnionRule("A2","BDoubleA"),
                    "A2": ProductRule("AtomA","AutantAB", "".join),
                    "B": UnionRule("B2","ADoubleB"),
                    "B2": ProductRule("AtomB","AutantAB", "".join),
                    "BDoubleA": ProductRule("AtomB","DoubleA", "".join),
                    "ADoubleB": ProductRule ("AtomA","DoubleB", "".join),
                    "DoubleA": ProductRule ("A","A", "".join),
                    "DoubleB": ProductRule ("B","B", "".join),
                    "Vide": EpsilonRule(""),
                    "AtomA": SingletonRule("A"),
                    "AtomB": SingletonRule("B")}

    tGram = [treeGram, fiboGram, abWordGram, dyckGram, ab2MaxGram, palABGram, palABCGram, autantABGram]

    for g in tGram:
        init_grammar(g)
    
    # for i in range(len(tGram)):
    #    print(str(i) + " : ")
    #    for key in tGram[i].keys():
    #        print("    " + key+ " val : " + str(tGram[i][key].valuation()))

    gram = "AutantAB"
    N = 8
    ID = 7

    c = tGram[ID][gram].count(N)
    print("count : " + str(c))
    
    lt = tGram[ID][gram].list(N)
    for el in lt:
        print(el)
    
    if c != 0:
        assert ([lt[i] == tGram[ID][gram].unrank(N,i) for i in range(len(lt))])

    # print(tGram[1]['Fib'].unrank(6,12))

    # Note : La taille ou poids d'un objet est le nombre d’atomes qu'il contient. Le poids d'un élément
    # correspondant à une paire (e1; e2) est donc la somme des poids de e1 et de e2


