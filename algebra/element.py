from abc import ABC, abstractmethod

class GroupElement(ABC):
    def __init__(self, word=None):
        self.word = word or []
    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass
