import numpy as np
from math import sqrt

from QFA.MM_1QFA import MM_1QFA
from QFA.LanguageGenerator import LanguageGenerator
from QFA.LanguageChecker import LanguageChecker
from QFA.Plotter import Plotter


def main():

    # 71753663.pdf example 2.3.5
    # Freivalds_9_1.pdf strona 45

    p = 0.682327803828019

    alphabet = 'ab'

    initial_state = np.array([[sqrt(1-p)], [sqrt(p)], [0], [0]])

    a_matrix = np.array([[1-p,           sqrt(p*(1-p)), 0, -sqrt(p)],
                         [sqrt(p*(1-p)), p,             0, sqrt(1-p)],
                         [0,             0,             1, 0],
                         [sqrt(p),       -sqrt(1-p),    0, 0]])

    b_matrix = np.array([[0, 0, 0, 1],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [1, 0, 0, 0]])

    end_matrix = np.array([[0, 0, 0, 1],
                           [0, 0, 1, 0],
                           [0, 1, 0, 0],
                           [1, 0, 0, 0]])

    measurement_acc = np.array([[0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 0]])

    measurement_rej = np.array([[0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 0],
                                [0, 0, 0, 1]])

    qfa = MM_1QFA(alphabet, initial_state, [a_matrix, b_matrix, end_matrix], measurement_acc, measurement_rej)

    language_generator = LanguageGenerator('a*b*', alphabet)

    language, not_in_language = language_generator.get_language_sample()
    print(language)

    language_checker = LanguageChecker(qfa, language, not_in_language)

    plotter = Plotter(language_checker)
    plotter.plot()


if __name__ == "__main__":
    main()
