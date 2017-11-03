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
    if cpt == n:
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

    test = {"Mdr": UnionRule("Mdr", "Mdr")}

    init_grammar(treeGram)
    # print (treeGram['Tree']._grammar['Node'].valuation())
    init_grammar(fiboGram)
    # print (fiboGram['AtomA']._grammar['CasBAu'].valuation())
    
    # for t in treeGram['Tree'].list(4):
    #    print(t)

    # for t in fiboGram['Fib'].list(4):
    #    print(t)
    
    print(treeGram['Node'].unrank(6,12))
    # print(fiboGram['Vide'].unrank(0,0))


    # Test count
    #for key in fiboGram.keys():
    #    print(key + " : ")
    #    for i in range(11):
    #        print("    "+str(fiboGram[key].count(i)))

    # init_grammar(test)
    # Puis on l'init mais c'est un effet de bord car ils appellent la grammaire:
    # fiboGram['Fib'].count(3)
    # sans avoir fait:
    # fiboGram['Fib'] = init_grammar(fiboGram)

    # Donc init_grammar(fiboGram)
    #     Ne renvoit pas forcément un nouvel objet de type AbstractRule.
    #     Utilise la methode set de l'object Abstractrules pour modifier fiboGram


    # Note : La taille ou poids d'un objet est le nombre d’atomes qu'il contient. Le poids d'un élément
    # correspondant à une paire (e1; e2) est donc la somme des poids de e1 et de e2


