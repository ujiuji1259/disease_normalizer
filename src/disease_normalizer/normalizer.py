import os

from . import utils
from .converter import dnorm, exact_matcher, fuzzy_matcher
from .base_converter import BaseConverter

BASE_URL = "http://aoi.naist.jp/norm/MANBYO_SABC.csv"

class Normalizer(object):
    def __init__(self, preprocessor, converter):
        self.load_manbyo_dict()

        # load converter
        if isinstance(converter, str):
            if converter == "exact":
                self.converter = exact_matcher.ExactMatchConverter(self.manbyo_dict)
            elif converter == "fuzzy":
                self.converter = fuzzy_matcher.FuzzyMatchConverter(self.manbyo_dict)
            else:
                self.converter = dnorm.dnorm_converter.DNormConverter(self.manbyo_dict)
        elif isinstance(converter, BaseConverter):
            self.converter = converter
        else:
            assert NotImplementedError, "Please specify converter by selecting (exact|fuzzy|dnorm) or creating your own converter inheriting BaseConverter"

    def load_manbyo_dict(self):
        DEFAULT_CACHE_PATH = os.getenv("DEFAULT_CACHE_PATH", "~/.cache")
        DEFAULT_MANBYO_PATH = Path(os.path.expanduser(
                        os.path.join(DEFAULT_CACHE_PATH, "norm")
                ))
        DEFAULT_MANBYO_PATH.mkdir(parents=True, exist_ok=True)

        if not (DEFAULT_MANBYO_PATH / "MANBYO_SABC.csv").exists():
            utils.download_fileobj(BASE_URL, DEFAULT_MANBYO_PATH / "MANBYO_SABC.csv")

        self.manbyo_dict = utils.load_dict(DEFAULT_MANBYO_PATH / "MANBYO_SABC.csv")


    def normalize(self, words):
        pass
