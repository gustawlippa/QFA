from QFA.Automata import Automata


class LanguageChecker:
    def __init__(self,
                 automata: Automata,
                 language: list,
                 not_in_language: list):
        self.language = language
        self.not_in_language = not_in_language
        self.automata = automata
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

    def run(self):
        self.lang_results = [self.automata.process(word) for word in self.language]
        self.not_lang_results = [self.automata.process(word) for word in self.not_in_language]

    def check_cutpoint(self):
        cutpoint = 1
        err = None
        if not self.lang_results or not self.not_lang_results:
            self.run()
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
