import matplotlib.pyplot as plt
import numpy as np

from QFA.LanguageChecker import LanguageChecker


class Plotter:
    def __init__(self, language_checker: LanguageChecker):
        self.language_checker = language_checker

    def plot(self):
        if not self.language_checker.lang_results:
            self.language_checker.run()

        probabilities_in_lang = [e[0] for e in self.language_checker.lang_results]
        probabilities_not_in_lang = [e[0] for e in self.language_checker.not_lang_results]

        try:
            n, bins, patches = plt.hist(probabilities_not_in_lang, bins='auto', range=(0, 1), alpha=0.5,
                                        label='Words not in language', color='red', edgecolor='black')
            n, bins, patches = plt.hist(probabilities_in_lang,  bins='auto', range=(0, 1), alpha=0.5,
                                        label='Words in language', color='green',edgecolor='black')
        except:
            n, bins, patches = plt.hist(probabilities_not_in_lang, bins=np.linspace(0, 1, 100), range=(0, 1), alpha=0.5,
                                        label='Words not in language', color='red', edgecolor='black')
            n, bins, patches = plt.hist(probabilities_in_lang, bins=np.linspace(0, 1, 100), range=(0, 1), alpha=0.5,
                                        label='Words in language', color='green', edgecolor='black')

        # for i, number in enumerate(n):
        #     plt.text(x = )
        plt.legend()
        plt.show()


if __name__ == "__main__":

    from QFA.MO_1QFA import mo_1qfa_example_4
    qfa = mo_1qfa_example_4()
    # from QFA.MM_1QFA import example
    # qfa = example()

    from QFA.LanguageGenerator import LanguageGenerator
    lg = LanguageGenerator('(aaa)*', 'a')
    l, ln = lg.get_language_sample()

    lang_checker = LanguageChecker(qfa, l, ln)

    p = Plotter(lang_checker)
    p.plot()


