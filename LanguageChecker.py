

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
            isolated_cutpoint, epsilon = result
            self.accepted.append(("isolated_cutpoint", isolated_cutpoint, epsilon))

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

        for word in self.language:
            p_for_word = self.automata.process(word)
            if p_for_word < cutpoint:
                cutpoint = p_for_word

        for word in self.not_in_language:
            p_for_word = self.automata.process(word)
            if p_for_word > cutpoint:
                return False

        return cutpoint

    def check_isolated_cutpoint(self):
        cutpoint_l = 1

        for word in self.language:
            p_for_word = self.automata.process(word)
            if p_for_word < cutpoint_l:
                cutpoint_l = p_for_word

        cutpoint_not_l = 0

        for word in self.not_in_language:
            p_for_word = self.automata.process(word)
            if p_for_word > cutpoint_not_l:
                cutpoint_not_l = p_for_word

        if cutpoint_l < cutpoint_not_l:
            return False

        cutpoint = (cutpoint_l - cutpoint_not_l) / 2
        epsilon = cutpoint_l - cutpoint
        return cutpoint, epsilon

    def check_monte_carlo(self):
        for word in self.language:
            p_for_word = self.automata.process(word)
            if p_for_word != 1:
                return False
        epsilon = 0
        for word in self.not_in_language:
            p_for_word = self.automata.process(word)
            if p_for_word > epsilon:
                epsilon = p_for_word

        if epsilon >= 1/2:
            return False

        return epsilon

    def check_bounded_error(self):
        epsilon = 0
        for word in self.language:
            p_for_word = self.automata.process(word)
            if p_for_word < 1 - epsilon:
                epsilon = 1 - p_for_word

        for word in self.not_in_language:
            p_for_word = self.automata.process(word)
            if p_for_word > epsilon:
                epsilon = p_for_word

        if epsilon >= 1/2:
            return False

        return epsilon

    def check_positive_unbounded(self):
        for word in self.language:
            p_for_word = self.automata.process(word)
            if p_for_word == 0:
                return False
        return True

    def check_negative_unbounded(self):
        for word in self.language:
            p_for_word = self.automata.process(word)
            if p_for_word != 1:
                return False

        return True
