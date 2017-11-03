# coding: utf-8
from rules.AbstractRule import AbstractRule

class ConstanteRule(AbstractRule):
    def __init__(self, object):
        super().__init__()
        self._object = object
    # Ici Epsilon Rules n'est pas connu...
    # Possiblement ça peut exploser
    def valuation(self):
        if(isinstance(self, self.subclass[0])):
            return 0
        else:
            return 1

    def unrank(self, n, r):
        c = self.count(n)
        if r >= c:
            raise ValueError("Le rang r (%d) doit etre strictement inférieur au nombre d'objets de taille %d (%d)"%(r,n,c))

        return self._object

class EpsilonRule(ConstanteRule):
    def __init__(self, object):
        super().__init__(object)
    
    def count(self, n):
        if n==0:
            return 1
        else:
            return 0
    
    def list(self, n):
        if n == 0:
            return [self._object]
        else:
            return []


class SingletonRule(ConstanteRule):
        def __init__(self, object):
            super().__init__(object)

        def count(self,n):
            if n==1:
                return 1
            else:
                return 0

        def list(self,n):
            if n == 1:
                return [self._object]
            else:
                return []


ConstanteRule.subclass =[EpsilonRule, SingletonRule]


if __name__ == '__test_classic__' or __name__ == '__main__':
    print("Cas de tests ConstanteRule:")
    a = object()
    b =  object()
    rule = ConstanteRule((a, b))
    assert (rule._grammar == {})
    assert (rule._object == (a, b))

    rule1 = EpsilonRule((a, b))
    rule2 = SingletonRule((a, b))
    b1 = isinstance(rule1, EpsilonRule) and issubclass(type(rule1), ConstanteRule)
    b2 = isinstance(rule2, SingletonRule) and issubclass(type(rule2), ConstanteRule)
    assert (b1 and rule1.valuation() == 0)
    assert (b2 and rule2.valuation() == 1)

    print("Pass")
