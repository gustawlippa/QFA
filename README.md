Na naszą bibliotekę składają się moduły odpowiadające pewnym
funkcjonalnościom albo automatom. Odpowiednie moduły oraz udostępniane
przez nie obiekty i funkcje wyglądają tak:

-   **PFA** (*Probabilistic Finite Automata*) to moduł odpowiadający za
    symulację PFA

    Jego główna klasa, *PFA*, zawiera metody:

    -   *init(alphabet, initialstate, transition_matrices,
        acceptance_vector)* - konstruktor automatu, przyjmuje jako
        argumenty alfabet, stan początkowy, macierze przejść oraz wektor
        akceptacji

    -   *process(word)* - symulacja pojedynczego słowa. Jako argument
        przyjmuje słowo, zwraca krotkę *(prawdopodobieństwo akceptacji,
        możliwy błąd)*

    W module dostępne są również przykładowe symulacje:

    -   *dfa_example()* - przykładowa symulacja DFA (*ang. Deterministic
        Finite Automata*)

    -   *pfa_example()* - przykładowa symulacja PFA

    -   *example()* - wywołuje oba wyżej wymienione przykłady

    Uruchomienie modułu spowoduje wywołanie funkcji *example()*.

-   **MO1QFA** (*Measure-Once Quantum Finite Automata*) to moduł
    odpowiadający za symulację MO-1QFA

    Jego główna klasa, *MO1QFA*, zawiera metody:

    -   *init(alphabet, initial_state, transition_matrices,
        projective_measurement)* - konstruktor automatu, przyjmuje jako
        argumenty alfabet, stan początkowy, macierze przejść oraz
        macierz reprezentującą końcowy pomiar

    -   *process(word)* - symulacja pojedynczego słowa. Jako argument
        przyjmuje słowo, zwraca krotkę *(prawdopodobieństwo akceptacji,
        możliwy błąd)*

    W module dostępne są również przykładowe symulacje:

    -   *mo_1qfa_example1()* - przykładowa symulacja

    -   *mo_1qfa_example2()* - przykładowa symulacja

    -   *mo_1qfa_example3()* - przykładowa symulacja

    -   *mo_1qfa_example4()* - przykładowa symulacja

    -   *example()* - wywołuje wszystkie wyżej wymienione przykłady

    Uruchomienie modułu spowoduje wywołanie funkcji *example()*.

-   **MM1QFA**(*Measure-Many Quantum Finite Automata*) to moduł
    odpowiadający za symulację MM-1QFA

    Jego główna klasa, *MM1QFA*, zawiera metody:

    -   *init(alphabet, initial_state, transition_matrices,
        projective_measurement_accept, projective_measurement_reject,
        projective_measurement_non)* - konstruktor automatu, przyjmuje
        jako argumenty alfabet, stan początkowy, macierze przejść oraz
        macierze pomiarów rzutowych. Argument *projectivemeasurementnon*
        jest opcjonalny - w przypadku podania jedynie macierzy
        rozpinających przestrzenie stanów akceptujących oraz
        odrzucających zostanie wyliczona automatycznie

    -   *process(word)* - symulacja pojedynczego słowa. Jako argument
        przyjmuje słowo, zwraca krotkę *(prawdopodobieństwo akceptacji,
        możliwy błąd)*

    W module dostępna jest również przykładowe symulacja *example()*.
    Uruchomienie modułu spowoduje wywołanie funkcji *example()*.

-   **GQFA** (*General Quantum Finite Automata*) to moduł odpowiadający
    za symulację GQFA

    Jego główna klasa, *GQFA*, zawiera metody:

    -   *init(alphabet, initial_state, transition_matrices,
        projective_measurements)* - Konstruktor automatu, przyjmuje jako
        argumenty alfabet, stan początkowy, macierze przejść oraz
        macierze pomiarów rzutowych (dla każdego symbolu alfabetu)

    -   *process(word)* - symulacja pojedynczego słowa. Jako argument
        przyjmuje słowo, zwraca krotkę *(prawdopodobieństwo akceptacji,
        możliwy błąd)*

    W module dostępna jest również przykładowa symulacja *example()*.
    Uruchomienie modułu spowoduje wywołanie funkcji *example()*.

-   **LanguageChecker** to moduł odpowiadający za sprawdzanie akceptacji
    języka przez dany automat przy różnych trybach działania

    Jego główna klasa, *LanguageChecker*, zawiera metody:

    -   *init(automata, language, not_in_language)* - konstruktor obiektu,
        przyjmuje jako argumenty zdefiniowany uprzednio automat, listę
        słów należących do języka oraz listę słów nienależących do
        języka

    -   *check_language()* - metoda sprawdzająca wszystkie tryby
        akceptacji języka. Zwraca słownik trybów akceptacji, przy
        których automat rozpoznaje język, gdzie kluczem jest nazwa a
        wartością parametry danego trybu. W przypadku, gdy automat nie
        rozpoznaje języka w danym trybie, nie występuje on w zwracanym
        słowniku. Możliwe jest sprawdzenie konkretnego trybu akceptacji,
        lecz zalecane jest używanie właśnie tej metody, gdyż zwraca
        pełną informację na temat badanego automatu

    -   *check_cutpoint()* - metoda sprawdzająca tryb akceptacji *z
        punktem odcięcia*. Zwraca *False*, jeżeli automat nie akceptuje
        języka w tym trybie, lub wartość punktu odcięcia, jeżeli
        akceptuje

    -   *check_isolated_cutpoint()* - metoda sprawdzająca tryb akceptacji
        *z odizolowanym punktem odcięcia*. Zwraca *False*, jeżeli
        automat nie akceptuje języka w tym trybie, lub krotkę
        ($\lambda$, $\epsilon$, wartość błędu) jeżeli akceptuje. W tym
        trybie, jeżeli wartość $\epsilon$ jest tego samego rzędu
        wielkości, co wartość błędu, nie jesteśmy w stanie jednoznacznie
        stwierdzić, czy automat rozpoznaje dany język

    -   *check_monte_carlo()* - metoda sprawdzająca tryb akceptacji
        *metodą Monte Carlo*. Zwraca *False*, jeżeli automat nie
        akceptuje języka w tym trybie, lub $\epsilon$, jeżeli akceptuje

    -   *check_bounded_error()* - metoda sprawdzająca tryb akceptacji *z
        ograniczonym błędem*. Zwraca *False*, jeżeli automat nie
        akceptuje języka w tym trybie, lub $\epsilon$, jeżeli akceptuje

    -   *check_positive_unbounded()* - metoda sprawdzająca tryb akceptacji
        *z pozytywnie jednostronnie nieograniczonym błędem*. Zwraca
        *False*, jeżeli automat nie akceptuje języka w tym trybie lub
        *True*, jeżeli akceptuje

    -   *check_negative_unbounded()* - metoda sprawdzająca tryb akceptacji
        *z negatywnie jednostronnie nieograniczonym błędem*. Zwraca
        *False*, jeżeli automat nie akceptuje języka w tym trybie lub
        *True*, jeżeli akceptuje

-   **LanguageGenerator** to moduł odpowiadający za generowanie słów
    należących oraz nienależących do języka

    Jego główna klasa, *LanguageGenerator*, zawiera metody:

    -   *init(regex, alphabet)* - konstruktor obiektu, przyjmuje jako
        argumenty wyrażenie regularne opisujące język oraz jego alfabet.
        Dodatkowo, jeżeli w wyrażeniu regularnym pojawi się ,,\\a”,
        zostanie on automatycznie podmieniony na ,,[alphabet]”, czyli
        klasę liter alfabetu, co pozwala na zwięźlejsze pisanie wyrażeń
        regularnych w wielu częstych przypadkach

    -   *get_language_sample(n, short_words_percent, max_len)* - metoda
        odpowiedzialna za generowanie próbki języka. Przyjmuje jako
        parametry ilość słów do wygenerowania, procentową zawartość
        krótkich słów w tym zbiorze oraz maksymalną długość słowa.
        Zwraca krotkę (słowa należące do języka, słowa nienależące do
        języka)

    W module dostępny jest również przykład generowania słów:

    -   *example()* - przykładowe generowanie słów należących oraz
        nienależących do języka

    Uruchomienie modułu spowoduje wywołanie funkcji *example()*.

-   **Plotter** to moduł odpowiadający za graficzne przedstawienie
    trybów akceptacji języka oraz ich parametrów

    Jego główna klasa, *Plotter* zawiera metody:

    -   *init(language_checker)* - konstruktor obiektu, przyjmuje jako
        argument obiekt klasy *LanguageChecker*

    -   *plot()* - metoda tworząca graficzne przedstawienie trybów
        akceptacji


