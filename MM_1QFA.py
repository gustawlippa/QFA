import numpy as np
from typing import List
from math import sqrt


class MM_1QFA:

    def __init__(self, alphabet: str,
                 initial_state: np.ndarray,
                 transition_matrices: List[np.ndarray],
                 projective_measurement_accept: np.ndarray,
                 projective_measurement_reject: np.ndarray,
                 projective_measurement_non: np.ndarray
                 ):
        # list of chars
        self.alphabet = alphabet
        # np column vector, initial dist over states
        self.initial_state = initial_state
        # list of np matrices - position in list corresponds to position of letter in alphabet,
        # perhaps a map could be better
        # watch out in MM_1QFA - there needs to be a transition matrix for the end symbol
        self.transition_matrices = transition_matrices
        # np matrix containing ones and zeroes
        self.projective_measurement_accept = projective_measurement_accept
        self.projective_measurement_reject = projective_measurement_reject
        self.projective_measurement_non = projective_measurement_non

    def process(self, word: str):

        total_state = (self.initial_state, 0, 0)

        for letter in word:
            # print("Letter:\t", letter, ", state before:\t", total_state)
            transition_matrix = self.transition_matrices[self.alphabet.index(letter)]
            state = total_state[0]

            continue_probability = self.projective_measurement_non @ transition_matrix @ state

            acceptance_probability = total_state[1]
            v = self.projective_measurement_accept @ transition_matrix @ state
            acceptance_probability += np.vdot(v, v)

            rejection_probability = total_state[2]
            v = self.projective_measurement_reject @ transition_matrix @ state
            rejection_probability += np.vdot(v, v)

            total_state = (continue_probability, acceptance_probability, rejection_probability)
            # print("Letter:\t", letter, ", state after:\t", total_state)

        # print("End sign:\t$, state:\t", total_state)
        transition_matrix = self.transition_matrices[-1]
        state = total_state[0]

        continue_probability = self.projective_measurement_non @ transition_matrix @ state

        acceptance_probability = total_state[1]
        v = self.projective_measurement_accept @ transition_matrix @ state
        acceptance_probability += np.vdot(v, v)

        rejection_probability = total_state[2]
        v = self.projective_measurement_reject @ transition_matrix @ state
        rejection_probability += np.vdot(v, v)

        total_state = (continue_probability, acceptance_probability, rejection_probability)

        # print("End state:\t", total_state)

        return total_state[1]


def example():
    alphabet = 'a'

    a_matrix = np.array([[1 / 2, 1/2, 0, 0],
                         [sqrt(1 / 2), -sqrt(1/2), (1 / 2), -sqrt(1/2)],
                         [(1 / 2), 1/2, 0, 0],
                         [0, 0, -sqrt(1/2), sqrt(1/2)]])

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

    qfa = MM_1QFA(alphabet, initial_state, [a_matrix, end_matrix], measurement_acc, measurement_rej, measurement_non)

    # print('MM_1QFA example:')
    # as I understand, it should return 1/2 as it does
    # res = qfa.process('a')
    # print('a\t', res)
    # example from QFA paper - returns 0.9785533905932737, which is 5/8+1/(2sqrt(2)) as in the paper
    # res = qfa.process('aa')
    # print('aa\t', res)
    return qfa
