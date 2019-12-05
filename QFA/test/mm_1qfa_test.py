import unittest
from QFA import MM_1QFA as MM
import numpy as np
from math import sqrt


class MM1QFATest(unittest.TestCase):

    def test_example(self):
        alphabet = 'a'

        a_matrix = np.array([[1 / 2, 1 / 2, sqrt(1 / 2), 0],
                             [sqrt(1 / 2), -sqrt(1 / 2), 0, 0],
                             [1 / 2, 1 / 2, -sqrt(1 / 2), 0],
                             [0, 0, 0, 1]])

        end_matrix = np.array([[0, 0, 0, 1],
                               [0, 0, 1, 0],
                               [1, 0, 0, 0],
                               [0, 1, 0, 0]])

        initial_state = np.array([[1], [0], [0], [0]])

        measurement_acc = np.array([[0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 0]])

        measurement_rej = np.array([[0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 1]])

        measurement_non = np.array([[1, 0, 0, 0],
                                    [0, 1, 0, 0],
                                    [0, 0, 0, 0],
                                    [0, 0, 0, 0]])

        qfa = MM.MM_1QFA(alphabet, initial_state, [a_matrix, end_matrix], measurement_acc, measurement_rej,
                      measurement_non)

        prob_a, err_a = qfa.process('a')
        self.assertAlmostEqual(prob_a, 1/2, delta=err_a)

        prob_aa, err_aa = qfa.process('aa')
        self.assertAlmostEqual(prob_aa, (5/8 + 1/(2*(sqrt(2)))), delta=err_aa)


if __name__ == '__main__':
    unittest.main()