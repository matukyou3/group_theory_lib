from abc import ABC, abstractmethod

class Group(ABC):
    @abstractmethod
    def generators(self):
        """群の生成元を返す"""
        pass
    
    @abstractmethod
    def multiply(self, a, b):
        pass
    
    @abstractmethod
    def identity(self):
        pass
    
    @abstractmethod
    def inverse(self, a):
        pass
    
    def elements(self):
        """有限群の場合のみ列挙可能"""
        raise NotImplementedError("無限群は列挙不可能")
    