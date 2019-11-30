import numpy as np
from typing import List
from math import sqrt


def get_complementary_matrix(list_of_matrices):
    size = list_of_matrices[0].shape[0]
    diag = np.eye(size)
    s = sum(list_of_matrices)
    return diag - s


def get_projective_measurements(list_of_matrices):
    # check input format
    if len(list_of_matrices[0]) == 3:
        # acc, rej and non matrices are provided
        for i, measurement in enumerate(list_of_matrices):
            size = measurement[0].shape[0]
            s = sum(measurement)
            if not np.array_equal(s, np.eye(size)):
                print(s, np.eye(size))
                raise Exception('Wrong ', i, 'th measurement')
        return list_of_matrices
    elif len(list_of_matrices[0]) == 2:
        # we have to calculate non halting matrix
        return [pair_of_matrices + [get_complementary_matrix(pair_of_matrices)] for pair_of_matrices in list_of_matrices]


def is_unitary(m):
    return np.allclose(np.eye(m.shape[0]), np.conjugate(m).T @ m)


def check_transition_matrices(matrices):
    if all([is_unitary(m) for m in matrices]):
        return matrices
    else:
        print([is_unitary(m) for m in matrices])
        raise Exception('Transition matrix is not unitary')


class GQFA:

    def __init__(self, alphabet: str,
                 initial_state: np.ndarray,
                 transition_matrices: List[np.ndarray],
                 projective_measurements: List[List[np.ndarray]]
                 ):
        # list of chars
        self.alphabet = alphabet
        # np column vector, initial dist over states
        self.initial_state = initial_state
        # list of np matrices - position in list corresponds to position of letter in alphabet,
        # perhaps a map could be better
        # watch out in GQFA - there needs to be a transition matrix for the end symbol
        self.transition_matrices = check_transition_matrices(transition_matrices)
        # list of lists of 2 np matrices containing ones and zeroes
        # first one should be accepting
        # second one should be rejecting
        # similarly as the list of transition matrices
        self.projective_measurements = get_projective_measurements(projective_measurements)

    def process(self, word: str):

        total_state = (self.initial_state, 0, 0)

        for letter in word:
            # print("Letter:\t", letter, ", state before:\t", total_state)
            transition_matrix = self.transition_matrices[self.alphabet.index(letter)]
            projective_measurements = self.projective_measurements[self.alphabet.index(letter)]
            projective_measurement_accept = projective_measurements[0]
            projective_measurement_reject = projective_measurements[1]
            projective_measurement_non = projective_measurements[2]

            state = total_state[0]

            continue_probability = projective_measurement_non @ transition_matrix @ state

            acceptance_probability = total_state[1]
            v = projective_measurement_accept @ transition_matrix @ state
            acceptance_probability += np.vdot(v, v)

            rejection_probability = total_state[2]
            v = projective_measurement_reject @ transition_matrix @ state
            rejection_probability += np.vdot(v, v)

            total_state = (continue_probability, acceptance_probability, rejection_probability)
            # print("Letter:\t", letter, ", state after:\t", total_state)

        # print("End sign:\t$, state:\t", total_state)
        transition_matrix = self.transition_matrices[-1]
        state = total_state[0]
        projective_measurements = self.projective_measurements[-1]
        projective_measurement_accept = projective_measurements[0]
        projective_measurement_reject = projective_measurements[1]
        projective_measurement_non = projective_measurements[2]

        continue_probability = projective_measurement_non @ transition_matrix @ state

        acceptance_probability = total_state[1]
        v = projective_measurement_accept @ transition_matrix @ state
        acceptance_probability += np.vdot(v, v)

        rejection_probability = total_state[2]
        v = projective_measurement_reject @ transition_matrix @ state
        rejection_probability += np.vdot(v, v)

        total_state = (continue_probability, acceptance_probability, rejection_probability)

        # print("End state:\t", total_state)
        error = abs(1 - acceptance_probability - rejection_probability)
        return total_state[1], error


def example():
    alphabet = 'a'

    a_matrix = np.array([[1/2,         1/2,        sqrt(1/2),  0],
                         [sqrt(1 / 2), -sqrt(1/2), 0,          0],
                         [1/2,         1/2,        -sqrt(1/2), 0],
                         [0,           0,          0,          1]])

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

    # this example is equivalent to MM_1QFA
    measurements = [[measurement_acc, measurement_rej], [measurement_acc, measurement_rej]]

    gqfa = GQFA(alphabet, initial_state, [a_matrix, end_matrix], measurements)

    print('GQFA example:')
    res = gqfa.process('a')
    print('a\t', res)
    res = gqfa.process('aa')
    print('aa\t', res)

    return gqfa


if __name__ == "__main__":
    example()
