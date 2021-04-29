from abc import ABCMeta, abstractmethod

class BaseConverter(metaclass=ABCMeta):
    @abstractmethod
    def convert(self):
        pass
