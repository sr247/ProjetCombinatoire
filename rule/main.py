# coding: utf-8

from ConstanteRule import *
from ConstructorRule import *
from ProductRule import *

from Tree import *
from UnionRule import *

from UnionRule import UnionRule

from ConstanteRule import *
from ProductRule import *


class Bound():
    def __init__(self, C, min, max):
        self._list = []
        self._count = []
        for i in range(min,max+1):
            self._list += C.list(i)
            self._count.append(C.count(i))
            
            
def convGramCond(gram, key):
    gram[key].conv(gram, key)


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
        for key in [ x for x in gram.keys() if isinstance(gram[x], ConstructorRule)]:
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
    
    # Fonctions principalement utilisées pour les Trees
    size = lambda tree : tree.size()
    isFst = lambda tree : not tree.is_leaf()
    pack = lambda obj: Node(obj[0], obj[1])
    unpack = lambda tree : (tree.left(), tree.right())


    # Exemple ici on déclare la grammaire Tree
    treeGram = {"Tree": UnionRule("Node", "Leaf", isFst, size),
                "Node": ProductRule("Tree", "Tree", pack, unpack, size),
                "Leaf": SingletonRule(Leaf)}



    # Exemple de grammaire condensée + conversion
    treeGramCond = {"Tree" : Union(Prod(NonTerm("Tree"), NonTerm("Tree"), pack, unpack, size), Singleton(Leaf), isFst,size)}
    convGramCond(treeGramCond,"Tree")

    # Ces fonctions sont utilisées dans la plus part des cas sur les grammaires fonctionnant avec des objets de type string
    size = lambda s: len(s)
    isEmpty = lambda s: s == ""
    unpack = lambda s: (s[:1], s[1:])  # Premier caractère et le reste
    unpack2 = lambda s: (s[:len(s) - 1], s[len(s) - 1])  # Tout sauf le dernier caractère et le dernier caractère
    isFstA = lambda s: s[:1] == 'A'
    isFstB = lambda s: s[:1] == 'B'
    single = lambda s: len(s) == 1
    join = "".join
    
    #Sequence Simple
    testSequence = {"SeqA" : Sequence(Singleton("a"), Epsilon(""), "".join, unpack2, isEmpty, size)}
    #testSequence = {"AorBx" : Union(Sequence(Singleton("a"), Epsilon(""), "".join, unpack2, isEmpty, size),Sequence(Singleton("b"), Epsilon(""), "".join, unpack2, isEmpty, size))}
    convGramCond(testSequence, "SeqA")
    # print(testSequence)

    #'SeqA': UnionRule("Eps-2", "Prod-3")
    #'Prod-3': ProductRule("SeqA", "AtomA")
    #'Sing-1': SingletonRule("a")
    #'Eps-2': EpsilonRule("")


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

    def unpackDyck(s) :
        g = 0
        ret = ""
        while g != -1 and s != "":
            tmp = s[:1]
            if tmp == "(" :
                g += 1
            elif tmp == ")":
                g -= 1
            if g != -1:
                ret += tmp
                s = s[1:]
        return ret,s
    #Quesiont 2.2.3
    dyckGram = {"DyckWord" : UnionRule("Vide","CasStart",isEmpty, size),
                "CasStart": ProductRule("AtomL","CasMid", join, unpack, size),
                "CasMid": ProductRule("DyckWord","CasEnd", join, unpackDyck, size),
                "CasEnd": ProductRule("AtomR","DyckWord", join, unpack, size),
                "Vide": EpsilonRule(""),
                "AtomL": SingletonRule("("),
                "AtomR": SingletonRule(")")}

    #Quesiont 2.2.4	
    ab2MaxGram = {"AB2Max": UnionRule("Vide", "Start", isEmpty, size),
                  "Start": UnionRule("CasA", "CasB", isFstA, size),
                  "CasA": ProductRule("AtomA", "StartedA", join, unpack, size),
                  "CasB": ProductRule("AtomB", "StartedB", join, unpack, size),
                  "StartedA": UnionRule("Vide", "NextA",isEmpty,size),
                  "StartedB": UnionRule("Vide", "NextB",isEmpty,size),
                  "NextA": UnionRule("CasB", "EndA", isFstB, size),
                  "NextB": UnionRule("CasA", "EndB", isFstA, size),
                  "FollowedByA": UnionRule("CasA", "Vide", isFstA, size),
                  "FollowedByB": UnionRule("CasB", "Vide", isFstB, size),
                  "EndA": ProductRule("AtomA", "FollowedByB", join, unpack, size),
                  "EndB": ProductRule("AtomB", "FollowedByA", join, unpack, size),
                  "Vide": EpsilonRule(""),
                  "AtomA": SingletonRule("A"),
                  "AtomB": SingletonRule("B")}

    #Quesiont 2.2.5.1
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
    
    #Quesiont 2.2.5.1
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


    # # Au niveau des méthodes size : un singleton ne vaus plus 1 caractère.. Problématique ?
    # HTML = {"Page": ProductRule("DOCTYPE", "HTML", join),
    #                 "HTML": ProductRule("O_HTML", "CONTEXT", join),
    #                 "CONTEXT": ProductRule("BALISES", "C_HTML", join),
    #
    #                 "BALISES": ProductRule("HEAD", "BODY", join),
    #
    #                 "HEAD": ProductRule("O_HEAD", "HEAD_CONTEXT", join),
    #                 "HEAD_CONTEXT": ProductRule("HEAD_TAG", "C_HEAD", join),
    #
    #                 "HEAD_TAG": UnionRule("META", "HEAD_OTHER1"),
    #                 "HEAD_OTHER1": UnionRule("TITLE", "HEAD_OTHER2"),
    #                 "HEAD_OTHER2": UnionRule("LINK", "HEAD_OTHER3"),
    #                 "HEAD_OTHER3": UnionRule("STYLE", "SCRIPT"),
    #
    #                 "META": SingletonRule("<meta charset=\"utf-8\" />"),
    #
    #                 "TITLE": ProductRule("O_TITLE", "TITLE_TEXT", join),
    #                 "TITLE_TEXT": ProductRule("TEXT", "C_TITLE", join),
    #
    #                 "LINK": SingletonRule(" <link src=\"file.css\" />"),
    #
    #                 "STYLE": SingletonRule("<link src=\"file.css\" />"),
    #
    #                 "SCRIPT": ProductRule("O_SCRIPT", "SCRIPT_CODE", join),
    #                 "SCRIPT_CODE" : ProductRule("CODE", "C_SCRIPT", join),
    #
    #                 "BODY": ProductRule("O_BODY", "BODY_TAG", join),
    #                 "BODY_TAG": ProductRule("BODY_TAG1", "C_BODY", join),
    #
    #                 "BODY_TAG1": UnionRule("PARA", "AREF"),
    #
    #                 "AREF": ProductRule("O_AREF", "AREF_TEXT", join),
    #                 "AREF_TEXT": ProductRule("TEXT", "C_AREF", join),
    #
    #                 "PARA": ProductRule("O_PARA", "PARA_TEXT", join),
    #                 "PARA_TEXT": ProductRule("TEXT", "C_PARA", join),
    #
    #                 "TEXT": SingletonRule(" Text "),
    #                 "CODE": SingletonRule("\t\t Code\n"),
    #
    #                 "DOCTYPE": SingletonRule("<!DOCTYPE html>\n"),
    #                 "O_HTML": SingletonRule("<html>\n"),
    #                 "C_HTML": SingletonRule("</html>\n"),
    #                 "O_HEAD": SingletonRule("\t<head>\n"),
    #                 "C_HEAD": SingletonRule("\t</head>\n"),
    #                 "O_TITLE": SingletonRule("\t\t<title>"),
    #                 "C_TITLE": SingletonRule("</title>\n"),
    #                 "O_SCRIPT": SingletonRule("\t\t<script>\n"),
    #                 "C_SCRIPT": SingletonRule("\t\t</script>\n"),
    #
    #                 "O_BODY": SingletonRule("\t<body>\n"),
    #                 "C_BODY": SingletonRule("\t</body>\n"),
    #                 "O_PARA": SingletonRule("\t\t<p>"),
    #                 "C_PARA": SingletonRule("</p>\n"),
    #                 "O_AREF": SingletonRule("\t\t<a href=\"link\">"),
    #                 "C_AREF": SingletonRule("</a>\n"),
    #                 "Vide": EpsilonRule("")}


    HTML = {"Page": ProductRule("DOCTYPE", "HTML", join),
            "HTML": ProductRule("O_HTML", "CONTEXT", join),
            "CONTEXT": ProductRule("CORE", "C_HTML", join),

            "CORE": ProductRule("HEAD", "BODY", join),

            "HEAD": ProductRule("O_HEAD", "HEAD_CONTEXT", join),
            "HEAD_CONTEXT": ProductRule("HEAD_CONTENT", "C_HEAD", join),

            "HEAD_CONTENT": UnionRule("HEAD_TAG", "Vide"),

            "HEAD_TAG": UnionRule("META_TAG", "HEAD_OTHER1"),
            "HEAD_OTHER1": UnionRule("TITLE_TAG", "HEAD_OTHER2"),
            "HEAD_OTHER2": UnionRule("LINK_TAG", "HEAD_OTHER3"),
            "HEAD_OTHER3": UnionRule("STYLE_TAG", "HEAD_OTHER4"),
            "HEAD_OTHER4": UnionRule("SCRIPT_TAG", ""),
            # "HEAD_OTHER4": UnionRule("SCRIPT", "HEAD_OTHER_END"),
            # "HEAD_OTHER_END": UnionRule("SCRIPT", "HEAD_OTHER_END"),

            "META_TAG": UnionRule("META", "Vide"),
            "META": SingletonRule("\t\t<meta charset=\"utf-8\" />\n"),

            "TITLE_TAG": UnionRule("TITLE", "Vide"),
            "TITLE": ProductRule("O_TITLE", "TITLE_TEXT", join),
            "TITLE_TEXT": ProductRule("TEXT", "C_TITLE", join),

            "LINK_TAG": UnionRule("LINK", "Vide"),
            "LINK": SingletonRule("\t\t<link src=\"file.css\" />\n"),

            "STYLE_TAG": UnionRule("STYLE", "Vide"),
            "STYLE": ProductRule("O_STYLE", "STYLE_CODE", join),
            "STYLE_CODE": ProductRule("CODE", "C_STYLE", join),

            "SCRIPT_TAG": UnionRule("SCRIPT", "Vide"),
            "SCRIPT": ProductRule("O_SCRIPT", "SCRIPT_CODE", join),
            "SCRIPT_CODE": ProductRule("CODE", "C_SCRIPT", join),


            "BODY": ProductRule("O_BODY", "BODY_CONTEXT", join),
            "BODY_CONTEXT": ProductRule("BODY_CONTENT", "C_BODY", join),

            "BODY_CONTENT": UnionRule("BODY_TAG", "Vide"),

            "BODY_TAG": UnionRule("PARA_TAG", "AREF_TAG"),
            # "BODY_OTHER1": UnionRule("AREF", "BODY_TAG"),
            
            "AREF_TAG": UnionRule("SCRIPT", "Vide"),
            "AREF": ProductRule("O_AREF", "AREF_TEXT", join),
            "AREF_TEXT": ProductRule("TEXT", "C_AREF", join),

            "PARA_TAG": UnionRule("PARA", "Vide"),
            "PARA": ProductRule("O_PARA", "PARA_TEXT", join),
            "PARA_TEXT": ProductRule("TEXT", "C_PARA", join),


            "TEXT": UnionRule("Vide", "TEXT_TEXT"),
            "TEXT_TEXT": SingletonRule("Text"),
            "CODE": UnionRule("Vide", "TEXT_CODE"),
            "TEXT_CODE": SingletonRule("\t\t\tCode\n"),

            "DOCTYPE": SingletonRule("<!DOCTYPE html>\n"),
            "O_HTML": SingletonRule("<html>\n"),
            "C_HTML": SingletonRule("</html>\n"),
            "O_HEAD": SingletonRule("\t<head>\n"),
            "C_HEAD": SingletonRule("\t</head>\n"),
            "O_TITLE": SingletonRule("\t\t<title>"),
            "C_TITLE": SingletonRule("</title>\n"),
            "O_STYLE": SingletonRule("\t\t<style>\n"),
            "C_STYLE": SingletonRule("\t\t</style>\n"),
            "O_SCRIPT": SingletonRule("\t\t<script>\n"),
            "C_SCRIPT": SingletonRule("\t\t</script>\n"),

            "O_BODY": SingletonRule("\t<body>\n"),
            "C_BODY": SingletonRule("\t</body>\n"),
            "O_PARA": SingletonRule("\t\t<p>"),
            "C_PARA": SingletonRule("</p>\n"),
            "O_AREF": SingletonRule("\t\t<a href=\"link\">"),
            "C_AREF": SingletonRule("</a>\n"),
            "Vide": EpsilonRule("")}

    name = ["Page", "SeqA", "Tree", "Tree", "Fib", "ABWord", "DyckWord", "AB2Max", "PalAB", "PalABC", "AutantAB"]

    tGram = [HTML, testSequence, treeGram, treeGramCond, fiboGram, abWordGram, dyckGram, ab2MaxGram, palABGram,
             palABCGram, autantABGram]

    if len(name) != len(tGram):
        raise Exception("Nombre de grammaires différent du nombre de noms")
    
    for g in tGram:
        init_grammar(g)

    N = 3
    l = dyckGram['DyckWord'].list(N)
    for i in range(dyckGram['DyckWord'].count(N)-1):
        assert(dyckGram['DyckWord'].rank(l[i]) == i)
    #b = Bound(test['Tree'],0,4)
    #for el in b._list:
    #    print(el)

    for n in range(15):
        for i in range(HTML["Page"].count(n)):
            print("list n°%d : élément n°%d\n"%(n,i), HTML["Page"].list(n)[i])
    #start = time.time()
    #print(tGram[0]['Tree'].count(13))
    #end = time.time()
    #print(end-start)

    # Affiche les valeurs des valuations de tGram[i]
    # for key in tGram[1].keys():
    #     print(key, ":", tGram[1][key].valuation())
