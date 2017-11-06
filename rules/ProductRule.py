# coding: utf-8
from rules.ConstructorRule import ConstructorRule
from functools import lru_cache
from rules.ConstanteRule import Epsilon
from rules.UnionRule import UnionRule


class ProductRule(ConstructorRule):

        # On ne peut pas faire rank sur AutantAB avec notre grammaire actuelle
        # On a donc décidé de mettre ces fonctions en options
        # Si elles ne sont pas fourni, alors on ne peut pas faire de rank sur la grammaire correspondant
    def __init__(self, fst, snd, cons, unpack = None, size = None):
        super().__init__((fst,snd))
        # Constructeur de l'objet
        self._constructor = cons
        # Sépare l'objet den 2 sous-objets
        # Ex : Node(Leaf,Leaf) renvoie Leaf,Leaf
        self.unpack = unpack
        # Renvoie la taille de l'objet
        self.size = size

    def __repr__(self):
        return "ProductRule("+str(self._parameters[0])+", "+ str(self._parameters[1]) +")"

    def __str__(self):
        return "ProductRule("+str(self._parameters[0])+", "+ str(self._parameters[1]) +")"

    def _calc_valuation(self):
        valGauche = self._grammar[self._parameters[0]].valuation()
        valDroite = self._grammar[self._parameters[1]].valuation()
        return valGauche+valDroite

    @lru_cache(maxsize=32)
    def count(self,i):
        res = 0
        for k in range(i+1):
            l = i-k
            if k >= self._grammar[self._parameters[0]].valuation():
                if l >= self._grammar[self._parameters[1]].valuation():
                    cG = self._grammar[self._parameters[0]].count(k)  
                    cD = self._grammar[self._parameters[1]].count(l)  
                    res += cG*cD
        return res

    @lru_cache(maxsize=32)
    def list(self,i):
        res = []
        for k in range(i+1):
            l = i-k
            if k >= self._grammar[self._parameters[0]].valuation():
                if l >= self._grammar[self._parameters[1]].valuation():
                    lG = self._grammar[self._parameters[0]].list(k)  
                    lD = self._grammar[self._parameters[1]].list(l)  
                    for g in lG:
                        for d in lD:
                            res.append(self._constructor((g, d)))
        return res

    @lru_cache(maxsize=32)
    def unrank(self,n,r):        
        c = self.count(n)        
        if r >= c:
            raise ValueError("Le rang r (%d) doit etre strictement inférieur au nombre d'objets de taille %d (%d)"%(r,n,c))
        
        acc = 0
        cG =  0
        cD = 0
        for k in range(n+1):
            l = n-k
            if k >= self._grammar[self._parameters[0]].valuation():
                if l >= self._grammar[self._parameters[1]].valuation():
                    cG = self._grammar[self._parameters[0]].count(k)  
                    cD = self._grammar[self._parameters[1]].count(l)             
                    acc += cG*cD
            if r < acc:
                acc -= cG*cD
                break
        
        i = k
        j = r - acc

        # cf. Prog unrank sur bintree avec catalan
        k = self._grammar[self._parameters[1]].count(n - i)
        q,r = j//k, j%k

        mG = self._grammar[self._parameters[0]].unrank(i,q)
        mD = self._grammar[self._parameters[1]].unrank(n-i,r)  

        return self._constructor((mG,mD))


    def rank(self, obj):
        # On ne peut pas faire rank sur AutantAB avec notre grammaire actuelle
        # On a donc décidé de mettre ces fonctions en options
        # Si elles ne sont pas fourni, alors on ne peut pas faire de rank sur la grammaire correspondant    
        if self.unpack is None or self.size is None :
            raise Exception("Rank n'est pas autorisé sur cette grammaire")

        g,d = self.unpack(obj)
        
        n = self.size(obj)
        nG = self.size(g)
        rG = self._grammar[self._parameters[0]].rank(g)
        rD = self._grammar[self._parameters[1]].rank(d)
        acc = 0
        
        # Par exemple pour Tree
        # On compte le nombre d'objet dont la taille a gauche est inférieur a notre objet
        # Et la taille de droite supérieur (ordre lex donc, les arbres qui précèdent)
        # Avec l'exemple du sujet de unrank :
        # Node(Node(Node(Leaf, Node(Leaf, Leaf)), Leaf), Node(Node(Leaf, Leaf), Leaf)) 
        # n = 7, nG = 4, rG = 3, rD = 1
        # Tree(0)*Tree(7) 0 * 132
        # Tree(1)*Tree(6) 1 * 42
        # Tree(2)*Tree(5) 1 * 14
        # Tree(3)*Tree(4) 2 * 5
        # acc = 66
        # On se décale ensuite de l'offset formé du rang de l'arbre de gauche multiplié par le nombre d'arbre de droite, puis on ajoute le rang de l'arbre de droite
        # acc = 66 + rG * count(3) == 66 + (3*2)
        # acc = 72
        # acc + rD => rank = 73
    
        for k in range(nG):
            l = n - k
            cG = self._grammar[self._parameters[0]].count(k)
            cD = self._grammar[self._parameters[1]].count(l)
            acc += cG*cD
        acc += rG * self._grammar[self._parameters[1]].count(n - nG) 
        return acc + rD


class NonTerm():
    def __init__(self,str):
        self._str = str

    def __repr__(self):
        return self._str

    def __str__(self):
        return self._str

    def conv(self, gram):
        if gram[self._str] is None:
            raise Exception("NonTerm "+self._str + " n'est pas dans la grammaire")
        return self._str    

class Prod():
    def __init__(self,fst,snd,cons,unpack = None,size=None):
        self.prod = (fst,snd,cons,unpack,size)
    
    def __repr__(self):
        return "Prod("+str(self.prod[0])+", "+ str(self.prod[1]) +")"
    
    def __str__(self):
        return "Prod("+str(self.prod[0])+", "+ str(self.prod[1]) +")"

    def conv(self,gram, key = None):
        fst,snd,cons,unpack,size = self.prod
        
        k1 = fst.conv(gram)
        k2 = snd.conv(gram)
        # On vérifie que cette règle n'est pas déjà dans la grammaire
        for k in gram.keys():
            if isinstance(gram[k],ProductRule):
                if gram[k]._parameters[0] == k1 and gram[k]._parameters[1] == k2 and gram[k]._constructor == cons:
                    return k
        if key is None:
            key = "Prod-"+str(len(gram))
        gram[key] = ProductRule(k1,k2,cons,unpack,size)
        return key

class Sequence():
    def __init__(self,nonterm,vide,cons,unpack = None, isFst = None, size=None):
        self.prod = (nonterm,vide,cons,unpack, isFst ,size)
    
    def __repr__(self):
        return "Sequence("+str(self.prod[0])+", "+ str(self.prod[1]) +")"
    
    def __str__(self):
        return "Sequence("+str(self.prod[0])+", "+ str(self.prod[1]) +")"

    def conv(self,gram, key = None):
        nonterm,vide,cons,unpack,isFst,size = self.prod
        k2 = Epsilon(vide).conv(gram)
        if key is None:
            key = "Seq-"+str(len(gram))
        kp = Prod(NonTerm(key), NonTerm(nonterm), cons, unpack, size)
        kp = kp.conv(gram)
            
        gram[key] = UnionRule(k2, kp, isFst, size)
        return key
        
        
if __name__ == '__test_classic__' or __name__ == '__main__':
    print("Cas de tests ProductRule:")

    print("Pass")

