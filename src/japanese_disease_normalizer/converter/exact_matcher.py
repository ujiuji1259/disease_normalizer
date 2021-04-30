"""Converter using exact match

Convert disease using exact match.
"""
import csv
from .. import utils
from .base_converter import BaseConverter

class ExactMatchConverter(BaseConverter):
    """ExactMatcher

    Args:
        dictionary List[DictEntry]: manbyo dictionary

    Attributes:
        dict Dict[str: DictEntry]: manbyo dictionary
    """
    def __init__(self, dictionary):
        self.dict = {d.name: d for d in dictionary}

    def convert(self, word):
        """Convert surface form of the dictionary into the normalized form

        Args:
            word str: surface form of the disease

        Returns:
            DictEntry: normalized form of the input disease.
        """
        return self.dict.get(word, utils.DictEntry(None, None, None, None)), 1 if word in self.dict else 0
