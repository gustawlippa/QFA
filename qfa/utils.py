from qfa.automata import Automaton
import re
import random
import math
import matplotlib.pyplot as plt
import numpy as np


class LanguageChecker:
    def __init__(self,
                 automaton: Automaton,
                 language: list,
                 not_in_language: list):
        self.language = language
        self.not_in_language = not_in_language
        self.automaton = automaton
        self.accepted = {}
        self.lang_results = []
        self.not_lang_results = []

    def check_language(self):

        self.run()

        cutpoint = self.check_cutpoint()
        if cutpoint:
            self.accepted['cutpoint'] = cutpoint

        result = self.check_isolated_cutpoint()
        if result:
            isolated_cutpoint, epsilon, error = result
            self.accepted['isolated_cutpoint'] = (isolated_cutpoint, epsilon, error)

        monte_carlo_eps = self.check_monte_carlo()
        if monte_carlo_eps:
            self.accepted['Monte_Carlo'] = monte_carlo_eps

        bounded_err = self.check_bounded_error()
        if bounded_err:
            self.accepted['bounded'] = bounded_err

        positive = self.check_positive_unbounded()
        if positive:
            self.accepted['positive_unbounded'] = True

        negative = self.check_negative_unbounded()
        if negative:
            self.accepted['negative_unbounded'] = True

        return self.accepted

    def run(self):
        self.lang_results = [self.automaton.process(word) for word in self.language]
        self.not_lang_results = [self.automaton.process(word) for word in self.not_in_language]

    def check_cutpoint(self):
        cutpoint = 1
        err = None
        if not self.lang_results or not self.not_lang_results:
            self.run()
        if not self.lang_results:
            raise Exception("Cannot calculate cutpoint because there are no words in the language")
        for (p_for_word, err_for_word) in self.lang_results:
            if p_for_word < cutpoint:
                cutpoint = p_for_word
                err = err_for_word

        for (p_for_word, err_for_word) in self.not_lang_results:
            if p_for_word > cutpoint + err + err_for_word:
                return False

        return cutpoint

    def check_isolated_cutpoint(self):
        cutpoint_l = 1
        err = None
        if not self.lang_results or not self.not_lang_results:
            self.run()

        for (p_for_word, err_for_word) in self.lang_results:
            if p_for_word < cutpoint_l:
                cutpoint_l = p_for_word
                err = err_for_word

        cutpoint_not_l = 0
        err_not_l = None
        for (p_for_word, err_for_word) in self.not_lang_results:
            if p_for_word > cutpoint_not_l:
                cutpoint_not_l = p_for_word
                err_not_l = err_for_word

        error = max(err, err_not_l)
        cutpoint = (cutpoint_l + cutpoint_not_l) / 2
        epsilon = cutpoint - cutpoint_not_l

        if cutpoint_not_l > cutpoint + error:
            return False
        else:
            return cutpoint, epsilon, error

    def check_monte_carlo(self):
        if not self.lang_results or not self.not_lang_results:
            self.run()

        for (p_for_word, err_for_word) in self.lang_results:
            if p_for_word < 1 - err_for_word or p_for_word > 1 + err_for_word:
                return False
        epsilon = 0
        error = None
        for (p_for_word, err_for_word) in self.not_lang_results:
            if p_for_word > epsilon:
                epsilon = p_for_word
                error = err_for_word

        if epsilon >= 1/2 - error:
            return False

        return epsilon

    def check_bounded_error(self):
        epsilon = 0
        if not self.lang_results or not self.not_lang_results:
            self.run()

        for (p_for_word, err_for_word) in self.lang_results:
            if p_for_word < 1 - epsilon - err_for_word:
                epsilon = 1 - p_for_word - err_for_word

        for (p_for_word, err_for_word) in self.not_lang_results:
            if p_for_word > epsilon + err_for_word:
                epsilon = p_for_word + err_for_word

        if epsilon >= 1/2:
            return False

        return epsilon

    def check_positive_unbounded(self):
        if not self.lang_results:
            self.run()

        for (p_for_word, err_for_word) in self.lang_results:
            if 0 - err_for_word < p_for_word < 0 + err_for_word:
                return False
        return True

    def check_negative_unbounded(self):
        if not self.lang_results:
            self.run()

        for (p_for_word, err_for_word) in self.lang_results:
            if p_for_word < 1 - err_for_word or p_for_word > 1 + err_for_word:
                return False

        return True


class LanguageGenerator:

    def __init__(self,
                 regex: str,
                 alphabet: str):

        regex = parse_alphabet(alphabet, regex)

        self.regex = regex
        self.alphabet = alphabet

    def get_language_sample(self, n=100, short_words_percent=30, max_len=100):
        words = []
        not_in_lang = []
        in_lang = []
        p = re.compile(self.regex)

        short_words = math.ceil(n*short_words_percent/100)
        long_words = n*(100-short_words_percent)//100

        if len(self.alphabet) > 1:
            short_words_border = math.ceil(math.log(short_words, len(self.alphabet)))
        else:
            short_words_border = short_words*2

        if long_words > (max_len - short_words_border)**len(self.alphabet):
            max_len = long_words * 2 + short_words_border

        for i in range(n):
            dec = random.random()
            border = short_words_border
            if dec > short_words_percent/100:
                border = max_len

            w = get_random_word(self.alphabet, random.randint(0, border))
            while w in words:
                dec = random.random()
                border = short_words_border
                if dec > short_words_percent/100:
                    border = max_len

                w = get_random_word(self.alphabet, random.randint(0, border))
            words.append(w)

        for w in words:
            if p.fullmatch(w) is not None:
                in_lang.append(w)
            else:
                not_in_lang.append(w)

        return in_lang, not_in_lang


class Plotter:
    def __init__(self, language_checker: LanguageChecker):
        self.language_checker = language_checker

    def plot(self):
        if not self.language_checker.lang_results:
            self.language_checker.check_language()

        probabilities_in_lang = [e[0] for e in self.language_checker.lang_results]
        probabilities_not_in_lang = [e[0] for e in self.language_checker.not_lang_results]

        try:
            if len(probabilities_not_in_lang) > 100:
                n, bins, patches = plt.hist(probabilities_not_in_lang, bins='auto', range=(0, 1), alpha=0.5,
                                            label='Words not in language', color='red', edgecolor='black')
            else:
                n, bins, patches = plt.hist(probabilities_not_in_lang, bins=100, range=(0, 1), alpha=0.5,
                                            label='Words not in language', color='red', edgecolor='black')
            if len(probabilities_in_lang) > 100:
                n, bins, patches = plt.hist(probabilities_in_lang,  bins='auto', range=(0, 1), alpha=0.5,
                                        label='Words in language', color='green', edgecolor='black')
            else:
                n, bins, patches = plt.hist(probabilities_in_lang,  bins=100, range=(0, 1), alpha=0.5,
                                        label='Words in language', color='green', edgecolor='black')
        except:
            n, bins, patches = plt.hist(probabilities_not_in_lang, bins=np.linspace(0, 1, 100), range=(0, 1), alpha=0.5,
                                        label='Words not in language', color='red', edgecolor='black')
            n, bins, patches = plt.hist(probabilities_in_lang, bins=np.linspace(0, 1, 100), range=(0, 1), alpha=0.5,
                                        label='Words in language', color='green', edgecolor='black')

        min_ylim, max_ylim = plt.ylim()

        if 'isolated_cutpoint' in self.language_checker.accepted:
            ctp = self.language_checker.accepted['isolated_cutpoint'][0]
            eps = self.language_checker.accepted['isolated_cutpoint'][1]
            plt.axvline(ctp, color='k')
            plt.text(ctp, max_ylim * 1.01, 'Cutpoint: {:.2f}'.format(ctp), horizontalalignment='center', rotation=60)
            plt.axvline(ctp + eps, color='k', linestyle='dashed')
            plt.text(ctp + eps, max_ylim * 1.01, 'Cutpoint+$\epsilon$: {:.2f}'.format(ctp + eps),
                     horizontalalignment='center', rotation=60)
            plt.axvline(ctp - eps, color='k', linestyle='dashed')
            plt.text(ctp - eps, max_ylim * 1.01, 'Cutpoint-$\epsilon$: {:.2f}'.format(ctp - eps),
                     horizontalalignment='center', rotation=60)
        elif 'cutpoint' in self.language_checker.accepted:
            ctp = self.language_checker.accepted['cutpoint']
            plt.axvline(ctp, color='k')
            plt.text(ctp, max_ylim * 1.01, 'Cutpoint: {:.2f}'.format(ctp), horizontalalignment='center', rotation=60)
        if 'Monte_Carlo' in self.language_checker.accepted:
            eps = self.language_checker.accepted['Monte_Carlo']
            plt.axvline(1 / 2 + eps, color='k', linestyle='dashed')
            plt.text(1 / 2 + eps, max_ylim * 1.01, 'Monte Carlo boundary: {:.2f}'.format(1 / 2 + eps),
                     horizontalalignment='center', rotation=60)
            plt.axvline(1 / 2 - eps, color='k', linestyle='dashed')
            plt.text(1 / 2 - eps, max_ylim * 1.01, 'Monte Carlo boundary: {:.2f}'.format(1 / 2 - eps),
                     horizontalalignment='center', rotation=60)

        plt.ylabel('Word count')
        plt.xlabel('Acceptance probability')

        plt.legend()
        plt.show()


def parse_alphabet(alphabet, regex):
    return re.sub(r'\a', lambda match: '['+alphabet+']', regex)


def get_random_word(alphabet, length):
    w = random.sample(alphabet * length, length)
    return ''.join(w)



