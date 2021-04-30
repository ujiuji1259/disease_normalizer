import jaconv
from .base_preprocessor import BasePreprocessor

class IdenticalPreprocessor(BasePreprocessor):
    def __init__(self):
        pass

    def preprocess(self, word):
        return [word]

class FullWidthPreprocessor(BasePreprocessor):
    def __init__(self):
        pass

    def preprocess(self, word):
        result = [jaconv.h2z(word, kana=True, digit=True, ascii=True)]
        return result

class NFKCPreprocessor(BasePreprocessor):
    def __init__(self):
        pass

    def preprocess(self, word):
        result = [jaconv.normalize(word, 'NFKC')]
        return result
