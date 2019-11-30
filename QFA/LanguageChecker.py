

class LanguageChecker:
    def __init__(self, automata,
                 language: list,
                 not_in_language: list):
        self.language = language
        self.not_in_language = not_in_language
        self.automata = automata
        self.accepted = []

    def check_language(self):
        cutpoint = self.check_cutpoint()
        if cutpoint:
            self.accepted.append(("cutpoint", cutpoint))

        result = self.check_isolated_cutpoint()
        if result:
            isolated_cutpoint, epsilon, error = result
            self.accepted.append(("isolated_cutpoint", isolated_cutpoint, epsilon, error))

        monte_carlo_eps = self.check_monte_carlo()
        if monte_carlo_eps:
            self.accepted.append(("Monte_Carlo", monte_carlo_eps))

        bounded_err = self.check_bounded_error()
        if bounded_err:
            self.accepted.append(("bounded_error", bounded_err))

        positive = self.check_positive_unbounded()
        if positive:
            self.accepted.append("positive_unbounded")

        negative = self.check_negative_unbounded()
        if negative:
            self.accepted.append("negative unbounded")

    def check_cutpoint(self):
        cutpoint = 1
        err = None
        for word in self.language:
            p_for_word, err_for_word = self.automata.process(word)
            if p_for_word < cutpoint:
                cutpoint = p_for_word
                err = err_for_word

        for word in self.not_in_language:
            p_for_word, err_for_word = self.automata.process(word)
            if p_for_word > cutpoint + err + err_for_word:
                return False

        return cutpoint

    def check_isolated_cutpoint(self):
        cutpoint_l = 1
        err = None

        for word in self.language:
            p_for_word, err_for_word = self.automata.process(word)
            if p_for_word < cutpoint_l:
                cutpoint_l = p_for_word
                err = err_for_word

        cutpoint_not_l = 0
        err_not_l = None
        for word in self.not_in_language:
            p_for_word, err_for_word = self.automata.process(word)
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
        for word in self.language:
            p_for_word, err = self.automata.process(word)
            if p_for_word < 1 - err or p_for_word > 1 + err:
                return False
        epsilon = 0
        error = None
        for word in self.not_in_language:
            p_for_word, err = self.automata.process(word)
            if p_for_word > epsilon:
                epsilon = p_for_word
                error = err

        if epsilon >= 1/2 - error:
            return False

        return epsilon

    def check_bounded_error(self):
        epsilon = 0
        for word in self.language:
            p_for_word, err = self.automata.process(word)
            if p_for_word < 1 - epsilon - err:
                epsilon = 1 - p_for_word - err

        for word in self.not_in_language:
            p_for_word, err = self.automata.process(word)
            if p_for_word > epsilon + err:
                epsilon = p_for_word + err

        if epsilon >= 1/2:
            return False

        return epsilon

    def check_positive_unbounded(self):
        for word in self.language:
            p_for_word, err = self.automata.process(word)
            if 0 - err < p_for_word < 0 + err:
                return False
        return True

    def check_negative_unbounded(self):
        for word in self.language:
            p_for_word, err = self.automata.process(word)
            if p_for_word < 1 - err or p_for_word > 1 + err:
                return False

        return True
