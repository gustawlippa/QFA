from qfa.automata import GQFA, MM_1QFA as MM, PFA
from qfa.utils import LanguageChecker as Checker, LanguageGenerator


def main():
    pfa = PFA.example()
    # MO.example()
    mm_1qfa = MM.example()
    gqfa = GQFA.example()

    mm_checker = Checker.LanguageChecker(mm_1qfa, ["aa"], ["a"])
    mm_checker.check_language()
    print('MM-1QFA', mm_checker.accepted)

    pfa_checker = Checker.LanguageChecker(pfa, ["aa"], ["ab"])
    pfa_checker.check_language()
    print('PFA', pfa_checker.accepted)

    gqfa_checker = Checker.LanguageChecker(gqfa, ["aa", "aaa"], ["a"])
    gqfa_checker.check_language()
    print('GQFA', gqfa_checker.accepted)

    lg = LanguageGenerator('(aa)*', 'a')
    l, nl = lg.get_language_sample()
    gqfa_checker_generated = Checker.LanguageChecker(gqfa, l, nl)
    gqfa_checker_generated.check_language()
    print('GQFA 2', gqfa_checker_generated.accepted)


if __name__ == "__main__":
    main()
