from abc import ABCMeta, abstractmethod

class BasePreprocessor(metaclass=ABCMeta):
    @abstractmethod
    def preprocess(self):
        pass
