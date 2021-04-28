import csv
from .. import utils

class ExactMatchConverter(object):
    def __init__(self, dictionary):
        self.dict = {d.name: d for d in dictionary}

    def convert(self, word):
        return self.dict.get(word, utils.DictEntry(None, None, None, None))
