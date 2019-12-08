from QFA.GQFA import GQFA
from QFA.LanguageGenerator import LanguageGenerator
from QFA.LanguageChecker import LanguageChecker
from QFA.LanguageGenerator import get_random_word

import numpy as np
from math import sqrt
import time
from scipy.stats import unitary_group
import matplotlib.pyplot as plt


def qfa():

    alphabet = 'abcd'

    initial_state = np.array([[1], [0], [0], [0]])


    a_matrix = np.array([[1 / 2, 1 / 2, sqrt(1 / 2), 0],
                             [sqrt(1 / 2), -sqrt(1 / 2), 0, 0],
                             [1 / 2, 1 / 2, -sqrt(1 / 2), 0],
                             [0, 0, 0, 1]])

    b_matrix = np.array([[1 / 2, 1 / 2, sqrt(1 / 2), 0],
                             [sqrt(1 / 2), -sqrt(1 / 2), 0, 0],
                             [1 / 2, 1 / 2, -sqrt(1 / 2), 0],
                             [0, 0, 0, 1]]).T

    c_matrix = np.array([[sqrt(1 / 2), 0, sqrt(1 / 2), 0],
                             [0, sqrt(1 / 2), 0, sqrt(1 / 2)],
                             [sqrt(1 / 2), 0, -sqrt(1 / 2), 0],
                             [0, sqrt(1 / 2), 0, -sqrt(1 / 2)]])

    d_matrix = np.array([[sqrt(1 / 2), 0, sqrt(1 / 2), 0],
                             [0, sqrt(1 / 2), 0, sqrt(1 / 2)],
                             [sqrt(1 / 2), 0, -sqrt(1 / 2), 0],
                             [0, sqrt(1 / 2), 0, -sqrt(1 / 2)]]).T

    measurement_1 = np.array([[0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 0]])

    measurement_2 = np.array([[0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 1]])

    measurement_3 = np.array([[1, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 1]])
    measurement_4 = np.array([[1, 0, 0, 0],
                                [0, 1, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 1]])

    measurement_5 = np.array([[1, 0, 0, 0],
                                [0, 1, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]])

    end_matrix = np.array([[0, 0, 0, 1],
                               [0, 0, 1, 0],
                               [1, 0, 0, 0],
                               [0, 1, 0, 0]])

    gqfa = GQFA(alphabet, initial_state, [a_matrix, b_matrix, c_matrix, d_matrix, end_matrix], [[measurement_1, measurement_2]]*5)
    return gqfa, alphabet


def load_test(gqfa, alphabet):
    [do_load_test(gqfa, alphabet, words_no) for words_no in [100, 1000, 10000]]


def do_load_test(automata,alphabet,  words_no, n=1):
    lg = LanguageGenerator('(ab)*c?(d|a)*', alphabet)
    l, nl = lg.get_language_sample(words_no)
    print('got')
    print('mean length', np.mean([len(w) for w in l+nl]))
    lc = LanguageChecker(automata, l, nl)
    print('created', words_no, 'words')
    import time
    t_s = time.time()
    for i in range(n):
        lc.check_language()

    t_e = time.time()
    print('time in s:', t_e - t_s)
    print('one execution: ', (t_e - t_s)/(words_no))


def linear_w_len_test(gqfa, alphabet):

    # l, nl = lg.get_language_sample(10000)
    # print('got')
    # lc = LanguageChecker(gqfa, l, nl)
    # print('created')
    import time
    # for i in range(10):
    #     lc.check_language()

    # lc.check_language()

    n = 50

    word_lengths = [1,10,100,1000, 10000, 100000, 1000000]

    [do_test(gqfa, alphabet,  word_length, n) for word_length in word_lengths]


def do_test(automata, alphabet,  w_l, n):
    l = [get_random_word(alphabet, w_l) for i in range(n)]
    print('Language done')

    lc = LanguageChecker(automata, l, l)

    print('Checkers created')

    t_s = time.time()
    lc.check_language()
    t_e = time.time()
    print('word length ', w_l)
    print('time in s:', t_e - t_s)
    print('one execution time: ', (t_e - t_s)/(n*2))

    return (t_e - t_s)/(n*2)


def unitary_size_test():
    sizes = [i for i in range(10, 500, 50)]
    alphabet = 'abcd'

    res = []
    rep_no = 5
    for size in sizes:

        initial_state = np.zeros((size, size))
        initial_state[0, 0] = 1

        acc_measure = np.zeros((size, size))
        acc_measure[-1,-1] = 1

        rej_measure = np.zeros((size, size))
        rej_measure[-2,-2] = 1

        measurements = [[acc_measure, rej_measure] for i in range(len(alphabet)+1)]
        result_tmp = 0
        print('Automata size', size)

        for rep in range(rep_no):
            random_matrix = unitary_group.rvs(size)
            transition_matrices = [random_matrix for l in range(len(alphabet)+1)]
            qfa = GQFA(alphabet, initial_state,transition_matrices, measurements)
            result_tmp += do_test(qfa, alphabet, 1000, 1)

        res.append((size, result_tmp/rep_no))

    plt.xlabel('Automata size')
    plt.ylabel('Execution time (1 word, length 1000)')
    x,y = list(zip(*res))
    plt.plot(x,y)
    plt.show()


def main():
    gqfa, alphabet = qfa()
    # linear_w_len_test(gqfa, alphabet)
    load_test(gqfa, alphabet)


if __name__ =="__main__":
    # main()
    unitary_size_test()