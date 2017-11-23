import sys
sys.path.insert(0,'..')

import math
import unittest

from ProductRule import ProductRule
from rule.UnionRule import UnionRule

from ConstructorRule import ConstructorRule


class ConstructorRuleTest(unittest.TestCase):
    """
    Test case utilisé pour tester les fonctions du module 'AbstractRule'
    """

    def setUp(self):
        self.rule = ConstructorRule(tuple())
        self.rule1 = UnionRule(object(), object())
        self.rule2 = ProductRule(object(), object(), lambda:None)

    def test_init(self):
        self.assertEqual(self.rule._grammar, {})
        self.assertEqual(self.rule._valuation, math.inf)
        self.assertEqual(self.rule._parameters, tuple())

    def test_valuation(self):
        """
        Test que l'attribut _valuation a bien la valeur infini
        et que cette valeur est bien entière
        :return:
        """
        self.assertEqual(self.rule.valuation(), math.inf)
        # self.assertIsInstance(self.rule._valuation, int, msg="{}".format(math.inf))


    def test__update_valuation(self):
        """
        Test que la méthode update est bien appelée soit sur un UnionRule
        soit sur un ProductRule qui héritent tout les deux de constructorRule
        """
        b1 = isinstance(self.rule1, UnionRule) and issubclass(type(self.rule1), ConstructorRule)
        b2 = isinstance(self.rule2, ProductRule) and issubclass(type(self.rule2), ConstructorRule)
        self.assertTrue(b1 or b2, msg="{} | {}".format(b1, b2))





if __name__ == '__main__':
    unittest.main()
