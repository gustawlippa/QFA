import numpy as np
from typing import List
from math import sqrt

from QFA.Automata import Automata


class PFA(Automata):
    def __init__(self, alphabet: str,
                 initial_state: np.ndarray,
                 transition_matrices: List[np.ndarray],
                 acceptance_vector: np.ndarray):

        # list of chars
        self.alphabet = alphabet
        # np row vector, initial dist over states
        self.initial_state = initial_state
        # list of np matrices - position in list corresponds to position of letter in alphabet,
        # perhaps a map could be better
        self.transition_matrices = transition_matrices
        # np column vector of ones and zeroes
        self.acceptance_vector = acceptance_vector

    def process(self, word: str) -> (float, float):
        acceptance_probability = self.initial_state
        for letter in word:
            transition_matrix = self.transition_matrices[self.alphabet.index(letter)]
            acceptance_probability = acceptance_probability @ transition_matrix
        acceptance_probability = acceptance_probability @ self.acceptance_vector
        acceptance_probability = acceptance_probability[0][0]
        return acceptance_probability, 0


def example():
    dfa_example()
    res = pfa_example()
    return res


def dfa_example():
    alphabet = 'ab'
    # three states
    # symbol_matrix[i][j] - probability of going from state i to state j when reading symbol
    a_matrix = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    b_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    transition_matrices = [a_matrix, b_matrix]
    initial_state = np.array([[1, 0, 0]])
    acceptance_vector = np.array([[0], [0], [1]])

    pfa = PFA(alphabet, initial_state, transition_matrices, acceptance_vector)
    res_aa = pfa.process('aa')
    res_ab = pfa.process('ab')
    print('DFA example:')
    print('aa: ', res_aa, "\tab: ", res_ab)
    return pfa


def pfa_example():
    alphabet = 'ab'
    # three states
    # symbol_matrix[i][j] - probability of going from state i to state j when reading symbol
    a_matrix = np.array([[0, 0.5, 0.5], [0, 1, 0], [0, 0, 1]])
    b_matrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    transition_matrices = [a_matrix, b_matrix]
    initial_state = np.array([[1, 0, 0]])
    acceptance_vector = np.array([[0], [0], [1]])

    pfa = PFA(alphabet, initial_state, transition_matrices, acceptance_vector)
    res_aa = pfa.process('aa')
    res_ab = pfa.process('ab')
    print('PFA example:')
    print('aa: ', res_aa, "\tab: ", res_ab)
    return pfa


if __name__ == "__main__":
    example()
