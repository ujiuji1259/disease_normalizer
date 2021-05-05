"""Disease normalizer

Normalizer class normalizes disease names.
"""
import os
from pathlib import Path
from logging import getLogger

from . import utils
from .converter import exact_matcher, fuzzy_matcher
from .converter.dnorm import dnorm_converter
from .converter.base_converter import BaseConverter
from .preprocessor.pipeline import PreprocessorPipeline

BASE_URL = "http://aoi.naist.jp/norm/MANBYO_SABC.csv"

default_logger = getLogger(__name__)

class Normalizer(object):
    """Normalizer

    Args:
        preprocess_pipeline Union[PreprocessorPipeline, str]: pipeline of preprocessor. You can use str (basic|abbr)
        converter Union[BaseConverter, str]: converter for normalization. You can use str (exact|fuzzy|dnorm)
    """
    def __init__(self, preprocess_pipeline, converter, logger=None):
        self.logger = logger or default_logger
        # load preprocessor
        if isinstance(preprocess_pipeline, PreprocessorPipeline):
            self.preprocessor = preprocess_pipeline
        elif isinstance(preprocess_pipeline, str):
            self.logger.info("Try to use %s preprocess_pipeline", preprocess_pipeline)
            if preprocess_pipeline == "basic":
                self.preprocessor = PreprocessorPipeline(["NFKC", "fullwidth"])
                self.logger.info("Basic preprocess_pipeline runs NFKC and fullwidth preprocsessing")
            elif preprocess_pipeline == "abbr":
                self.preprocessor = PreprocessorPipeline(["abbr", "NFKC", "fullwidth"])
                self.logger.info("abbr preprocess_pipeline runs abbreviation expansion, NFKC and fullwidth preprocsessing")
            else:
                raise NotImplementedError("Please specify converter by selecting (basic) or creating your own converter inheriting BaseConverter")
        else:
            raise NotImplementedError("Please specify converter by selecting (basic) or creating your own preprocess pipeline instance")

        self.manbyo_dict = self.load_manbyo_dict()
        self.logger.info("Loaded %s entries", len(self.manbyo_dict))
        for entry in self.manbyo_dict:
            # 0番目を出現形として使用
            entry.name = self.preprocessor.preprocess(entry.name)[0]

        # load converter
        if isinstance(converter, str):
            self.logger.info("Try to use %s converter", converter)
            if converter == "exact":
                self.converter = exact_matcher.ExactMatchConverter(self.manbyo_dict)
            elif converter == "fuzzy":
                self.converter = fuzzy_matcher.FuzzyMatchConverter(self.manbyo_dict)
            elif converter == "dnorm":
                self.converter = dnorm_converter.DNormConverter(self.manbyo_dict)
            else:
                raise NotImplementedError("Please specify converter by selecting (exact|fuzzy|dnorm)")
        elif isinstance(converter, BaseConverter):
            self.logger.info("Try to use your own converter")
            self.converter = converter
        else:
            raise NotImplementedError("Please specify converter by selecting (exact|fuzzy|dnorm) or creating your own converter inheriting BaseConverter")

    def load_manbyo_dict(self):
        """Load manbyo dict

        This method create cache folder and download the manbyo dictionary.
        You can specify cache folder by setting environment variable "DEFAULT_CACHE_PATH"
        """
        DEFAULT_CACHE_PATH = os.getenv("DEFAULT_CACHE_PATH", "~/.cache")
        DEFAULT_MANBYO_PATH = Path(os.path.expanduser(
                        os.path.join(DEFAULT_CACHE_PATH, "norm")
                ))
        self.logger.info("Cache path: %s", str(DEFAULT_MANBYO_PATH))
        DEFAULT_MANBYO_PATH.mkdir(parents=True, exist_ok=True)

        if not (DEFAULT_MANBYO_PATH / "MANBYO_SABC.csv").exists():
            self.logger.info("Downloading manbyo dictionary from %s to %s", BASE_URL, str(DEFAULT_MANBYO_PATH / "MANBYO_SABC.csv"))
            utils.download_fileobj(BASE_URL, DEFAULT_MANBYO_PATH / "MANBYO_SABC.csv")

        manbyo_dict = utils.load_dict(DEFAULT_MANBYO_PATH / "MANBYO_SABC.csv")
        return manbyo_dict

    def normalize(self, word):
        """Normalize disease name

        We choose entry with maximum score if there are more than one entry that preprocessor creates (e.g. disambiguation of abbreviation expansion)

        Args:
            word str: target disease name

        Returns:
            DictEntry: linked entry of input disease name
        """
        self.logger.info("Input disease name: %s", word)
        preprocessed_words = self.preprocessor.preprocess(word)
        self.logger.info("Preprocessed disease name: %s", str(preprocessed_words))
        max_score = -float('inf')
        max_word = None
        for preprocessed_word in preprocessed_words:
            result, sim = self.converter.convert(preprocessed_word)
            if max_word is None or sim > max_score:
                max_score = sim
                max_word = result

        return max_word

