import numpy as np
from typing import List
from math import sqrt

from QFA.Automata import Automata


class MO_1QFA(Automata):

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
            # print("Letter:\t", letter, "\nLeft:\n", transition_matrix, "\nRight:\n", acceptance_probability)
            acceptance_probability = transition_matrix @ acceptance_probability

        # print("Measurement:\nLeft:\n", self.projective_measurement, "\nRight:\n", acceptance_probability)

        acceptance_probability = self.projective_measurement @ acceptance_probability

        acceptance_probability = np.vdot(acceptance_probability, acceptance_probability)  # vdot(a,a) = norm squared (a)

        return acceptance_probability, 0


def example():
    print('MO_1QFA examples:')
    mo_1qfa_example_1()
    mo_1qfa_example_2()
    qfa = mo_1qfa_example_3()
    return qfa


def mo_1qfa_example_1():
    alphabet = 'a'

    a_matrix = np.array([[sqrt(1/2), sqrt(1/2)], [sqrt(1/2), -sqrt(1/2)]])
    initial_state = np.array([[1], [0]])
    measurement = np.array([[0, 0], [0, 1]])

    qfa = MO_1QFA(alphabet, initial_state, [a_matrix], measurement)

    print('mo_qfa1')
    # it should return 1/2
    res = qfa.process('a')
    print('a\t', res)
    # example from QFA paper - returns 0 as should
    res = qfa.process('aa')
    print('aa\t', res)

    return qfa


def mo_1qfa_example_2():
    # example from wikipedia: (https://en.wikipedia.org/wiki/Quantum_finite_automata#Measure-once_automata)

    alphabet = '01'
    zero_matrix = np.array([[0, 1], [1, 0]])
    one_matrix = np.array([[1, 0], [0, 1]])
    projection_matrix = np.array([[1, 0], [0, 0]])

    initial_state = np.array([[1], [0]])

    qfa2 = MO_1QFA(alphabet, initial_state, [zero_matrix, one_matrix], projection_matrix)
    # should behave as DFA expecting words with even number of '0's
    print('mo_qfa2')
    print('111\t', qfa2.process('111'))
    print('101\t', qfa2.process('101'))
    print('001\t', qfa2.process('001'))
    print('\t', qfa2.process(''))

    return qfa2


def mo_1qfa_example_3():
    alphabet = '01'

    zero_matrix = np.array([[0, 1], [1, 0]])
    one_matrix = np.array([[1, 0], [0, 1]])
    projection_matrix = np.array([[1, 0], [0, 0]])

    # same example, but initial state is complex

    initial_state = np.array([[1/2+1j/2], [1/(2*sqrt(2))+1j/(2*sqrt(2))]])

    qfa3 = MO_1QFA(alphabet, initial_state, [zero_matrix, one_matrix], projection_matrix)
    # one must remember that initial state must be a quantum state, so it must comply with normalisation condition
    print('mo_qfa3')
    print('111\t', qfa3.process('111'))
    print('101\t', qfa3.process('101'))
    print('001\t', qfa3.process('001'))
    print('\t', qfa3.process(''))

    return qfa3


if __name__ == "__main__":
    example()
