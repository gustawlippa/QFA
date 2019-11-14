import numpy as np
from typing import List

from math import sqrt


class PFA:
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

    def process(self, word: str):
        acceptance_probability = self.initial_state
        for letter in word:
            transition_matrix = self.transition_matrices[self.alphabet.index(letter)]
            acceptance_probability = acceptance_probability @ transition_matrix
        acceptance_probability = acceptance_probability @ self.acceptance_vector
        return acceptance_probability


class MO_1QFA:

    def __init__(self, alphabet: str,
                 initial_state: np.ndarray,
                 transition_matrices: List[np.ndarray],
                 projective_measurement: np.ndarray):
        # list of chars
        self.alphabet = alphabet
        # np column vector, initial dist over states
        self.initial_state = initial_state
        # list of np matrices - position in list corresponds to position of letter in alphabet,
        # perhaps a map could be better
        self.transition_matrices = transition_matrices
        # np matrix containing ones and zeroes
        self.projective_measurement = projective_measurement

    def process(self, word: str):
        acceptance_probability = self.initial_state
        for letter in word:
            transition_matrix = self.transition_matrices[self.alphabet.index(letter)]
            # print("Left:\n", transition_matrix, "\nRight:\n", acceptance_probability)
            acceptance_probability = transition_matrix @ acceptance_probability

        acceptance_probability = self.projective_measurement @ acceptance_probability

        acceptance_probability = np.vdot(acceptance_probability, acceptance_probability)

        return acceptance_probability


def mo_1qfa_example():
    alphabet = 'a'

    a_matrix = np.array([[sqrt(1/2), sqrt(1/2)], [sqrt(1/2), -sqrt(1/2)]])
    initial_state = np.array([[1], [0]])
    measurement = np.array([[0, 0], [0, 1]])

    qfa = MO_1QFA(alphabet, initial_state, [a_matrix], measurement)

    # as I understand, it should return 1/2 as it does
    res = qfa.process('a')
    print('a\t', res)
    # example from QFA paper - returns 0 as should
    res = qfa.process('aa')
    print('aa\t', res)

    # example from wikipedia: (https://en.wikipedia.org/wiki/Quantum_finite_automata#Measure-once_automata)

    alphabet = '01'
    zero_matrix = np.array([[0, 1], [1, 0]])
    one_matrix = np.array([[1, 0], [0, 1]])
    projection_matrix = np.array([[1, 0], [0, 0]])

    initial_state = np.array([[1], [0]])

    qfa2 = MO_1QFA(alphabet, initial_state, [zero_matrix, one_matrix], projection_matrix)
    # should behave as DFA expecting words with even number of '0's
    print('qfa2')
    print('111\t', qfa2.process('111'))
    print('101\t', qfa2.process('101'))
    print('001\t', qfa2.process('001'))
    print('\t', qfa2.process(''))

    # same example, but initial state is complex

    initial_state = np.array([[1/2+1j/2], [1/(2*sqrt(2))+1j/(2*sqrt(2))]])

    qfa3 = MO_1QFA(alphabet, initial_state, [zero_matrix, one_matrix], projection_matrix)
    # should behave somehow
    # one must remember that initial state must be a quantum state, so it must comply with normalisation condition
    print('qfa3')
    print('111\t', qfa3.process('111'))
    print('101\t', qfa3.process('101'))
    print('001\t', qfa3.process('001'))
    print('\t', qfa3.process(''))


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
    print('aa: ', res_aa, "\tab: ", res_ab)


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
    print('aa: ', res_aa, "\tab: ", res_ab)


def main():
    # dfa_example()
    # pfa_example()
    mo_1qfa_example()


if __name__ == "__main__":
    main()
