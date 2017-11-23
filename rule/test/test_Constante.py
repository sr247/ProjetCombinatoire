import sys
sys.path.insert(0,'..')

import unittest

from ConstanteRule import ConstanteRule, EpsilonRule, SingletonRule


class ConstructorRuleTest(unittest.TestCase):
    """
    Test case utilisé pour tester les fonctions du module 'AbstractRule'
    """


    def setUp(self):
        self.rule = ConstanteRule(object())
        self.rule1 = EpsilonRule(object())
        self.rule2 = SingletonRule(object())
        self.n = [x for x in range(10)]

    def test_init(self):
        self.assertEqual(self.rule._grammar, {})
        self.assertEqual(type(self.rule._object), type(object()))


    def test_valuation(self):
        """
        Test que l'attribut _valuation a bien la valeur infini
        et que cette valeur est bien entière
        :return:
        """
        b1 = isinstance(self.rule1, EpsilonRule) and issubclass(type(self.rule1), ConstanteRule)
        b2 = isinstance(self.rule2, SingletonRule) and issubclass(type(self.rule2), ConstanteRule)
        self.assertTrue(b1 and self.rule1.valuation() == 0, msg="{}".format(b1))
        self.assertTrue(b2 and self.rule2.valuation() == 1, msg="{}".format(b1))

    def test_count(self):
        self.assertTrue(isinstance(self.rule1, EpsilonRule) and self.rule1.count(0) == 1)
        self.assertTrue(isinstance(self.rule1, EpsilonRule) and self.rule1.count(1) == 0)
        self.assertTrue(isinstance(self.rule1, EpsilonRule) and self.rule1.count(2) == 0)

        self.assertTrue(isinstance(self.rule2, SingletonRule) and self.rule2.count(2) == 0)
        self.assertTrue(isinstance(self.rule2, SingletonRule) and self.rule2.count(1) == 1)
        self.assertTrue(isinstance(self.rule2, SingletonRule) and self.rule2.count(0) == 0)


    def test_list(self):
        pass



if __name__ == '__main__':
    unittest.main()
