from abc import ABC, abstractmethod


class Automata(ABC):

    @abstractmethod
    def process(self, word: str) -> (float, float):
        pass
