from QFA import LanguageChecker as Checker, GQFA, MM_1QFA as MM, PFA as PFA


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

    gqfa_checker = Checker.LanguageChecker(gqfa, ["aa"], ["a"])
    gqfa_checker.check_language()
    print('GQFA', gqfa_checker.accepted)


if __name__ == "__main__":
    main()
