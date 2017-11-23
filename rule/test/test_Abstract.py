import sys
sys.path.insert(0,'..')

import unittest

from AbstractRule import AbstractRule


class AbstractRuleTest(unittest.TestCase):
    """
    Test case utilisé pour tester les fonctions du module 'AbstractRule'
    """

    def setUp(self):
        self.rule = AbstractRule()

    def test_init(self):
        self.assertEqual(self.rule._grammar, {})

    def test__set_grammar(self):
        a = object()
        self.rule._set_grammar({"Key": a})
        self.assertEqual (self.rule._grammar, {"Key": a})


if __name__ == '__main__':
    unittest.main()
