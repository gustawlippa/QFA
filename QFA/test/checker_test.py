import unittest
from QFA import LanguageChecker as Checker, GQFA


class LanguageCheckerTest(unittest.TestCase):
    def test_init(self):
        gqfa = GQFA.example()
        gqfa_checker = Checker.LanguageChecker(gqfa, ["aa", "aaa"], ["a"])

        self.assertEqual(gqfa_checker.automata, gqfa)


if __name__ == '__main__':
    unittest.main()
