import PFA as PFA
import MO_1QFA as MO
import MM_1QFA as MM
import GQFA
import LanguageChecker as Checker


def main():
    dfa = PFA.dfa_example()
    pfa = PFA.pfa_example()
    # MO.mo_1qfa_example()
    mm_1qfa = MM.example()
    gqfa = GQFA.example()

    mm_checker = Checker.LanguageChecker(mm_1qfa, ["aa"], ["a"])
    mm_checker.check_language()
    print(mm_checker.accepted)

    # pfa_checker = Checker.LanguageChecker(pfa, ["aa"], ["ab"])
    # pfa_checker.check_language()
    # print(pfa_checker.accepted)

    gqfa_checker = Checker.LanguageChecker(gqfa, ["aa"], ["a"])
    gqfa_checker.check_language()
    print(gqfa_checker.accepted)


if __name__ == "__main__":
    main()
