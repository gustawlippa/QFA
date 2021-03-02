import unittest
from QFA import LanguageChecker as Checker, GQFA


class LanguageCheckerTest(unittest.TestCase):
    def test_init(self):
        gqfa = GQFA.example()
        gqfa_checker = Checker.LanguageChecker(gqfa, ["aa", "aaa"], ["a"])

        self.assertEqual(gqfa_checker.automaton, gqfa)
        self.assertEqual(gqfa_checker.language, ["aa", "aaa"])
        self.assertEqual(gqfa_checker.not_in_language, ["a"])

    def test_gqfa_check(self):
        gqfa = GQFA.example()
        gqfa_checker = Checker.LanguageChecker(gqfa, ["aa", "aaa"], ["a"])
        gqfa_checker.check_language()

        self.assertIn('cutpoint', gqfa_checker.accepted)
        self.assertIn('isolated_cutpoint', gqfa_checker.accepted)
        self.assertIn('positive_unbounded', gqfa_checker.accepted)
        self.assertNotIn('Monte_Carlo', gqfa_checker.accepted)
        self.assertNotIn('bounded', gqfa_checker.accepted)
        self.assertNotIn('negative_unbounded', gqfa_checker.accepted)

        lambda_, epsilon, error = gqfa_checker.accepted['isolated_cutpoint']

        self.assertAlmostEqual(lambda_, 0.609375, delta=error)
        self.assertAlmostEqual(epsilon, 0.109375, delta=error)
        self.assertLess(error, 10**(-15))

        self.assertAlmostEqual(lambda_ + epsilon, gqfa_checker.accepted['cutpoint'], delta=error)


if __name__ == '__main__':
    unittest.main()
