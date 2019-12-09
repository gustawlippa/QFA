from QFA.GQFA import GQFA
from QFA.LanguageGenerator import LanguageGenerator
from QFA.LanguageChecker import LanguageChecker
from QFA.LanguageGenerator import get_random_word

import numpy as np
from math import sqrt
import time
from scipy.stats import unitary_group
import matplotlib.pyplot as plt


def random_qfa(n, alphabet):
    initial_state = np.zeros((n, n))
    initial_state[0, 0] = 1

    acc_measure = np.zeros((n, n))
    acc_measure[-1, -1] = 1

    rej_measure = np.zeros((n, n))
    rej_measure[-2, -2] = 1

    measurements = [[acc_measure, rej_measure] for i in range(len(alphabet) + 1)]

    random_matrix = unitary_group.rvs(n)
    transition_matrices = [random_matrix for l in range(len(alphabet) + 1)]
    qfa = GQFA(alphabet, initial_state, transition_matrices, measurements)

    return qfa


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

    n = 50

    word_lengths = [5, 10, 25, 50, 75, 100, 250, 500,750, 1000,2000,3000,4000, 5000,6000,7000,8000,9000, 10000]

    res = [(word_length, do_test(gqfa, alphabet,  word_length, n)) for word_length in word_lengths]

    plot(res, "Word length", "Time (s)")


def generated_words_test(gqfa,alphabet):
    n = 100

    word_lengths = [5, 10, 25, 50, 75, 100, 250, 500,750, 1000,2000,3000,4000, 5000]

    res = [(word_length, do_gen_test(gqfa, alphabet,  word_length, n)) for word_length in word_lengths]

    plot(res, "Word length", "Time (s)")


def do_gen_test(automata, alphabet,  w_l, n):
    lg = LanguageGenerator("\a*a[cde]*", alphabet)
    l, ln = lg.get_language_sample(n, max_len=w_l)
    print('Language done', len(l), ' ', len(ln) )

    lc = LanguageChecker(automata, l, ln)

    print('Checkers created')

    t_s = time.time()
    lc.check_language()
    t_e = time.time()
    print('word length ', w_l)
    print('time in s:', t_e - t_s)
    print('one execution time: ', (t_e - t_s)/(n*2))

    return (t_e - t_s)/(n*2)


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


def alphabet_len_test(automata_size):

    n = 500
    import string
    alpha = string.ascii_letters
    res = []
    al_lengths = range(1, 30)
    for len in al_lengths:
        alphabet = alpha[0:len]
        gqfa = random_qfa(automata_size, alphabet)

        res.append((len, do_test(gqfa, alphabet, 300, n)))

    plot(res, "Alphabet length", "Time (s)")


def unitary_size_test():
    sizes = [i for i in range(2, 50, 2)]
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
    plot(res, 'Automata size', 'Execution time (1 word, length 1000)')


def plot(res, xlabel, ylabel):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    x, y = list(zip(*res))
    plt.plot(x, y)
    plt.show()


def main():
    alphabet = "abcde"
    automata_size = 20
    gqfa = random_qfa(automata_size, alphabet)
    # linear_w_len_test(gqfa, alphabet)
    # generated_words_test(gqfa, alphabet)
    # alphabet_len_test(automata_size)
    # load_test(gqfa, alphabet)
    unitary_size_test()


if __name__ =="__main__":
    main()
