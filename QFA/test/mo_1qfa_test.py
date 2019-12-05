import unittest
from QFA import MO_1QFA as MO
import numpy as np
from math import sqrt, cos, sin, pi


class MO1QFATest(unittest.TestCase):

    def test_example1(self):
        alphabet = 'a'

        a_matrix = np.array([[sqrt(1 / 2), sqrt(1 / 2)], [sqrt(1 / 2), -sqrt(1 / 2)]])
        initial_state = np.array([[1], [0]])
        measurement = np.array([[0, 0], [0, 1]])

        qfa = MO.MO_1QFA(alphabet, initial_state, [a_matrix], measurement)

        prob_a, err_a = qfa.process('a')
        if err_a == 0:
            err_a = 1**(-15)
        self.assertAlmostEqual(prob_a, 1/2, delta=err_a)

        prob_aa, err_aa = qfa.process('aa')
        if err_aa == 0:
            err_aa = 1**(-15)
        self.assertAlmostEqual(prob_aa, 0, delta=err_aa)

    def test_example2(self):
        # example from wikipedia: (https://en.wikipedia.org/wiki/Quantum_finite_automata#Measure-once_automata)

        alphabet = '01'
        zero_matrix = np.array([[0, 1], [1, 0]])
        one_matrix = np.array([[1, 0], [0, 1]])
        projection_matrix = np.array([[1, 0], [0, 0]])

        initial_state = np.array([[1], [0]])

        qfa = MO.MO_1QFA(alphabet, initial_state, [zero_matrix, one_matrix], projection_matrix)
        # should behave as DFA expecting words with even number of '0's

        p_111, e_111 = qfa.process('111')
        p_101, e_101 = qfa.process('101')
        p_001, e_001 = qfa.process('001')
        p_, e_ = qfa.process('')

        self.assertAlmostEqual(p_111, 1, delta=e_111)
        self.assertAlmostEqual(p_101, 0, delta=e_101)
        self.assertAlmostEqual(p_001, 1, delta=e_001)
        self.assertAlmostEqual(p_, 1, delta=e_)

    def test_example3(self):
        alphabet = '01'

        zero_matrix = np.array([[0, 1], [1, 0]])
        one_matrix = np.array([[1, 0], [0, 1]])
        projection_matrix = np.array([[1, 0], [0, 0]])

        # same example, but initial state is complex

        initial_state = np.array([[1 / 2 + 1j / 2], [1 / (2 * sqrt(2)) + 1j / (2 * sqrt(2))]])

        qfa = MO.MO_1QFA(alphabet, initial_state, [zero_matrix, one_matrix], projection_matrix)
        # one must remember that initial state must be a quantum state, so it must comply with normalisation condition

        p_111, e_111 = qfa.process('111')
        p_101, e_101 = qfa.process('101')
        p_001, e_001 = qfa.process('001')
        p_, e_ = qfa.process('')

        self.assertAlmostEqual(p_111, 0.5 + 0j, places=15)
        self.assertAlmostEqual(p_101, 0.25 + 0j, places=15)
        self.assertAlmostEqual(p_001, 0.5 + 0j, places=15)
        self.assertAlmostEqual(p_, 0.5 + 0j, places=15)

    def test_example4(self):
        # This automaton should accept language L = {a^(3n)}
        # words in L should have acceptance probability 1
        alphabet = 'a'

        a_matrix = np.array([[cos(2 * pi / 3), -sin(2 * pi / 3)],
                             [sin(2 * pi / 3), cos(2 * pi / 3)]])

        end_matrix = np.eye(2)

        projection_matrix = np.array([[1, 0], [0, 0]])

        initial_state = np.array([[1], [0]])

        qfa = MO.MO_1QFA(alphabet, initial_state, [a_matrix, end_matrix], projection_matrix)

        from QFA.LanguageGenerator import LanguageGenerator
        lg = LanguageGenerator('(aaa)*', 'a')
        l, ln = lg.get_language_sample()
        error = 1**(-15)

        for w in l:
            p, e = qfa.process(w)
            self.assertAlmostEqual(p, 1, delta=max(error, e))

        for w in ln:
            p, e = qfa.process(w)
            self.assertAlmostEqual(p, 1/4, delta=max(error, e))

        p_a, e_a = qfa.process('a')
        p_aa, e_aa = qfa.process('aa')
        p_aaa, e_aaa = qfa.process('aaa')

        self.assertAlmostEqual(p_a, 1/4, delta=max(error, e_a))
        self.assertAlmostEqual(p_aa, 1/4, delta=max(error, e_aa))
        self.assertAlmostEqual(p_aaa, 1, delta=max(error, e_aaa))


if __name__ == '__main__':
    unittest.main()
