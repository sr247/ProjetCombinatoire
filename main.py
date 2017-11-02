# coding: utf-8

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
    absRule = AbstractRule(gram)
    absRule._set_grammar()

init_grammar(treeGram)
    
