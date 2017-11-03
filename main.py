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
                "Vide": EpsilonRule("\"\""),
                "CasAu": ProductRule("AtomA", "Fib", "".join),
                "AtomA": SingletonRule("A"),
                "AtomB": SingletonRule("B"),
                "CasBAu": ProductRule("AtomB", "CasAu", "".join)}
    
    #Quesiont 2.2.2
    abWordGram = {"ABWord": UnionRule("Vide", "StartAB"),
                  "StartAB": UnionRule("CasA", "CasB"),
                  "CasA": ProductRule("AtomA","ABWord", "".join),
                  "CasB": ProductRule("AtomB","ABWord", "".join),
                  "Vide": EpsilonRule("\"\""),
                  "AtomA": SingletonRule("A"),
                  "AtomB": SingletonRule("B")}
    #Quesiont 2.2.3
    dyckGram = {"DyckWord" : UnionRule("Vide","CasStart"),
                "CasStart": ProductRule("AtomL","CasMid", "".join),
                "CasMid": ProductRule("DyckWord","CasEnd", "".join),
                "CasEnd": ProductRule("AtomR","DyckWord", "".join),
                "Vide": EpsilonRule("\"\""),
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
                  "StartAB": UnionRule("CasA","CasB"),
                  "CasA": ProductRule("AtomA","EndA", "".join),
                  "CasB":	ProductRule("AtomB","EndB", "".join),
                  "EndA":	ProductRule("PalAB","AtomA", "".join),
                  "EndB":	ProductRule("PalAB","AtomB", "".join),
                  "Vide":	EpsilonRule(""),
                  "AtomA": SingletonRule("A"),
                  "AtomB": SingletonRule("B")}

    #Quesiont 2.2.5.2
    palABCGram = {"PalABC": UnionRule("Vide","StartABC"),
                  "StartABC": UnionRule("CasA","CasAutre"),
                  "CasAutre": UnionRule("CasB","CasC"),
                  "CasA": ProductRule("AtomA","EndA", "".join),
                  "CasB": ProductRule("AtomB","EndB", "".join),
                  "CasC": ProductRule("AtomC","EndC", "".join),
                  "EndA": ProductRule("PalABC","AtomA", "".join),
                  "EndB": ProductRule("PalABC","AtomB", "".join),
                  "EndC": ProductRule("PalABC","AtomC", "".join),
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

    N = 6

    lt = tGram[0]['Tree'].list(N)
    assert ([lt[i] == tGram[0]['Tree'].unrank(N,i) for i in range(len(lt))])

    # print(tGram[1]['Fib'].unrank(6,12))

    # Note : La taille ou poids d'un objet est le nombre d’atomes qu'il contient. Le poids d'un élément
    # correspondant à une paire (e1; e2) est donc la somme des poids de e1 et de e2


