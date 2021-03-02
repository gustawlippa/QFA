import unittest
from qfa.utils import LanguageGenerator


class LanguageGeneratorTest(unittest.TestCase):

    def test_init(self):
        lg = LanguageGenerator('[ca]+.\a*a[jk]?', 'abcdefghijk')
        self.assertEqual(lg.alphabet, 'abcdefghijk')
        self.assertEqual(lg.regex, "[ca]+.[abcdefghijk]*a[jk]?")

        lg2 = LanguageGenerator('(a|b|c)+\a?[def]*b', 'abcdef')
        self.assertEqual(lg2.alphabet, 'abcdef')
        self.assertEqual(lg2.regex, "(a|b|c)+[abcdef]?[def]*b")

    def test_generator_example_1(self):
        lg = LanguageGenerator('[ca]+.\a*a[jk]?', 'abcdefghijk')
        i, n = lg.get_language_sample(1000)

        self.assertGreater(len(i), 10)
        self.assertGreater(len(n), 100)

    def test_generator_example_2(self):
        lg = LanguageGenerator('[abc]*', 'abc')
        i, n = lg.get_language_sample(1000)

        self.assertEqual(len(i), 1000)
        self.assertEqual(len(n), 0)


if __name__ == '__main__':
    unittest.main()
