import os
from pathlib import Path

from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.measure.cosine import CosineMeasure
from simstring.database.dict import DictDatabase
from simstring.searcher import Searcher

from .. import utils


class FuzzyMatchConverter(object):
    def __init__(self, dictionary):
        self.dict = {d.name: d for d in dictionary}
        self.db = DictDatabase(CharacterNgramFeatureExtractor(2))
        [self.db.add(d) for d in self.dict.keys()]
        self.searcher = Searcher(self.db, CosineMeasure())

    def convert(self, word, alpha=0.5):
        results = self.searcher.ranked_search(word, alpha)
        if len(results) != 0:
            # results = [(sim, word), ...]
            return self.dict[results[0][1]]
        return utils.DictEntry(None, None, None, None)
