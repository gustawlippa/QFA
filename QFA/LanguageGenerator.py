import exrex as e
import re
import random
import math


def parse_alphabet(alphabet, regex):
    return re.sub(r'\a', lambda match: '['+alphabet+']', regex)


class LanguageGenerator:

    def __init__(self,
                 regex: str,
                 alphabet: str = None):

        if alphabet is not None:
            regex = parse_alphabet(alphabet, regex)
        # print('REGEX ', regex)

        self.regex = regex
        self.alphabet = alphabet

    def get_language_sample(self, n, short_words_percent=30):
        words = []
        not_in_lang = []
        in_lang = []
        p = re.compile(self.regex)

        short_words = math.ceil(n*short_words_percent/100)
        long_words = n*(1-short_words_percent)//100

        short_words_border = math.ceil(math.log(short_words, len(self.alphabet)))

        if long_words - short_words > 100:
            max_len = (long_words - short_words) * 2
        else:
            max_len = 100

        for i in range(n):
            dec = random.random()
            border = short_words_border
            if dec > short_words_percent/50:
                border = max_len

            w = get_random_word(self.alphabet, random.randint(0, border))
            while w in words:
                dec = random.random()
                border = short_words_border
                if dec > short_words_percent / 50:
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
    i, n = lg.get_language_sample(10000)
    # for w in i+n:
    #     print(len(w), w)
    print('Words in language: ', len(i))
    print('Words not in language: ', len(n))


if __name__ == "__main__":
    example()

