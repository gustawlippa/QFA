import unittest
from qfa.automata import PFA
import numpy as np


class PFATest(unittest.TestCase):

    def test_dfa(self):
        alphabet = 'ab'
        # three states
        # symbol_matrix[i][j] - probability of going from state i to state j when reading symbol
        a_matrix = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
        b_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        transition_matrices = [a_matrix, b_matrix]
        initial_state = np.array([[1, 0, 0]])
        acceptance_vector = np.array([[0], [0], [1]])

        pfa = PFA(alphabet, initial_state, transition_matrices, acceptance_vector)

        p_aa, e_aa = pfa.process('aa')
        p_ab, e_ab = pfa.process('ab')
        self.assertAlmostEqual(p_aa, 1, delta=e_aa)
        self.assertAlmostEqual(p_ab, 0, delta=e_ab)

    def test_pfa(self):
        alphabet = 'ab'
        # three states
        # symbol_matrix[i][j] - probability of going from state i to state j when reading symbol
        a_matrix = np.array([[0, 0.5, 0.5], [0, 1, 0], [0, 0, 1]])
        b_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        transition_matrices = [a_matrix, b_matrix]
        initial_state = np.array([[1, 0, 0]])
        acceptance_vector = np.array([[0], [0], [1]])

        pfa = PFA(alphabet, initial_state, transition_matrices, acceptance_vector)
        p_aa, e_aa = pfa.process('aa')
        p_ab, e_ab = pfa.process('ab')
        self.assertAlmostEqual(p_aa, 0.5, delta=e_aa)
        self.assertAlmostEqual(p_ab, 0.5, delta=e_ab)


if __name__ == '__main__':
    unittest.main()
