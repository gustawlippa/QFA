import re
import random
import math


def parse_alphabet(alphabet, regex):
    return re.sub(r'\a', lambda match: '['+alphabet+']', regex)


class LanguageGenerator:

    def __init__(self,
                 regex: str,
                 alphabet: str):

        regex = parse_alphabet(alphabet, regex)
        # print('REGEX ', regex)

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


def get_random_word(alphabet, length):
    w = random.sample(alphabet * length, length)
    return ''.join(w)


def example():
    lg = LanguageGenerator('[ca]+.\a*a[jk]?', 'abcdefghijk')
    i, n = lg.get_language_sample(1000)

    print('Words in language: ', len(i))
    print('Words not in language: ', len(n))


if __name__ == "__main__":
    example()

