from abc import ABC, abstractmethod


class Automaton(ABC):

    @abstractmethod
    def process(self, word: str) -> (float, float):
        pass
