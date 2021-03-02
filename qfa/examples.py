import numpy as np
from qfa.automata import PFA, MO_1QFA, MM_1QFA, GQFA
from qfa.utils import LanguageChecker, LanguageGenerator, Plotter
from math import sqrt, cos, sin, pi


def DFA_example():
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


def PFA_example():
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


def MO_1QFA_example_1():
    alphabet = 'a'

    a_matrix = np.array([[sqrt(1/2), sqrt(1/2)], [sqrt(1/2), -sqrt(1/2)]])
    initial_state = np.array([[1], [0]])
    measurement = np.array([[0, 0], [0, 1]])

    qfa = MO_1QFA(alphabet, initial_state, [a_matrix], measurement)

    print('MO_1QFA example 1:')
    # it should return 1/2
    res = qfa.process('a')
    print('a\t', res)
    # example from qfa paper - returns 0 as it should
    # the paper: https://www.researchgate.net/publication/264906610_Quantum_Finite_Automata
    #   Qiu, Daowen & Li, Lvzhou & Mateus, Paulo & Gruska, Jozef.
    #   (2012).
    #   Quantum Finite Automata. Handbook of Finite State Based Models and Applications.
    #   10.1201/b13055-7.
    res = qfa.process('aa')
    print('aa\t', res)

    return qfa


def MO_1QFA_example_2():
    # example from wikipedia: (https://en.wikipedia.org/wiki/Quantum_finite_automata#Measure-once_automata)

    alphabet = '01'
    zero_matrix = np.array([[0, 1], [1, 0]])
    one_matrix = np.array([[1, 0], [0, 1]])
    projection_matrix = np.array([[1, 0], [0, 0]])

    initial_state = np.array([[1], [0]])

    qfa2 = MO_1QFA(alphabet, initial_state, [zero_matrix, one_matrix], projection_matrix)
    # should behave like a DFA expecting words with an even number of '0's
    print('MO_1QFA example 2:')
    print('111\t', qfa2.process('111'))
    print('101\t', qfa2.process('101'))
    print('001\t', qfa2.process('001'))
    print('\t', qfa2.process(''))

    return qfa2


def MO_1QFA_example_3():
    alphabet = '01'

    zero_matrix = np.array([[0, 1], [1, 0]])
    one_matrix = np.array([[1, 0], [0, 1]])
    projection_matrix = np.array([[1, 0], [0, 0]])

    # same example as the mo_1qfa_example_2, but the initial state is complex

    initial_state = np.array([[1/2+1j/2], [1/(2*sqrt(2))+1j/(2*sqrt(2))]])

    qfa3 = MO_1QFA(alphabet, initial_state, [zero_matrix, one_matrix], projection_matrix)
    # one must remember that the initial state must be a quantum state, so it must comply with the normalisation
    # condition
    print('MO_1QFA example 3:')
    print('111\t', qfa3.process('111'))
    print('101\t', qfa3.process('101'))
    print('001\t', qfa3.process('001'))
    print('\t', qfa3.process(''))

    return qfa3


def MO_1QFA_example_4():
    # This automaton should accept the language L = {a^(3n)}
    # words in L should have the acceptance probability 1
    alphabet = 'a'

    a_matrix = np.array([[cos(2*pi/3), -sin(2*pi/3)],
                         [sin(2*pi/3), cos(2*pi/3)]])

    end_matrix = np.eye(2)

    projection_matrix = np.array([[1, 0], [0, 0]])

    initial_state = np.array([[1], [0]])

    qfa = MO_1QFA(alphabet, initial_state, [a_matrix, end_matrix], projection_matrix)

    print('MO_1QFA example 4:')
    print("a\t", qfa.process('a'))
    print("aa\t", qfa.process('aa'))
    print("aaa\t", qfa.process('aaa'))
    return qfa


def MM_1QFA_example():
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

    qfa = MM_1QFA(alphabet, initial_state, [a_matrix, end_matrix], measurement_acc, measurement_rej, measurement_non)

    print('MM_1QFA example:')
    # it should return 1/2
    res = qfa.process('a')
    print('a\t', res)
    # example from QFA paper - returns 0.9785533905932737, which is 5/8+1/(2sqrt(2)) as in the paper:
    # https://www.researchgate.net/publication/264906610_Quantum_Finite_Automata
    #   Qiu, Daowen & Li, Lvzhou & Mateus, Paulo & Gruska, Jozef.
    #   (2012).
    #   Quantum Finite Automata. Handbook of Finite State Based Models and Applications.
    #   10.1201/b13055-7.
    res = qfa.process('aa')
    print('aa\t', res)
    return qfa


def GQFA_example():
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


def LanguageGenerator_example():
    lg = LanguageGenerator('[ca]+.\a*a[jk]?', 'abcdefghijk')
    i, n = lg.get_language_sample(1000)

    print('LanguageGenerator example:')
    print('Words in language: ', len(i))
    print('Words not in language: ', len(n))


def Plotter_example():
    qfa = MO_1QFA_example_4()

    lg = LanguageGenerator('(aaa)*', 'a')
    l, ln = lg.get_language_sample()

    lang_checker = LanguageChecker(qfa, l, ln)

    p = Plotter(lang_checker)
    p.plot()


if __name__ == "__main__":
    DFA_example()
    PFA_example()
    MO_1QFA_example_1()
    MO_1QFA_example_2()
    MO_1QFA_example_3()
    MO_1QFA_example_4()
    MM_1QFA_example()
    GQFA_example()
