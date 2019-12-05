import unittest
from QFA import GQFA
import numpy as np
from math import sqrt


class GQFATest(unittest.TestCase):

    def test_example(self):
        # example is the same as in GQFA.example()
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

        measurements = [[measurement_acc, measurement_rej], [measurement_acc, measurement_rej]]

        gqfa = GQFA.GQFA(alphabet, initial_state, [a_matrix, end_matrix], measurements)

        prob_a, err_a = gqfa.process('a')
        self.assertAlmostEqual(prob_a, 0.5, delta=err_a)

        prob_aa, err_aa = gqfa.process('aa')
        self.assertAlmostEqual(prob_aa, (5/8 + 1/(2*sqrt(2))), delta=err_aa)


if __name__ == '__main__':
    unittest.main()
