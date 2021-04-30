"""Disease normalizer

Normalizer class normalizes disease names.
"""
import os
from pathlib import Path

from . import utils
from .converter import dnorm, exact_matcher, fuzzy_matcher
from .converter.base_converter import BaseConverter
from .preprocessor.pipeline import PreprocessorPipeline

BASE_URL = "http://aoi.naist.jp/norm/MANBYO_SABC.csv"

class Normalizer(object):
    """Normalizer

    Args:
        preprocess_pipeline Union[PreprocessorPipeline, str]: pipeline of preprocessor. You can use str (basic|abbr)
        converter Union[BaseConverter, str]: converter for normalization. You can use str (exact|fuzzy|dnorm)
    """
    def __init__(self, preprocess_pipeline, converter):
        # load preprocessor
        if isinstance(preprocess_pipeline, PreprocessorPipeline):
            self.preprocessor = preprocess_pipeline
        elif isinstance(preprocess_pipeline, str):
            if preprocess_pipeline == "basic":
                self.preprocessor = PreprocessorPipeline(["NFKC", "fullwidth"])
            if preprocess_pipeline == "abbr":
                self.preprocessor = PreprocessorPipeline(["abbr", "NFKC", "fullwidth"])
            else:
                assert NotImplementedError, "Please specify converter by selecting (basic) or creating your own converter inheriting BaseConverter"
        else:
            assert NotImplementedError, "Please specify converter by selecting (basic) or creating your own preprocess pipeline instance"

        self.manbyo_dict = self.load_manbyo_dict()
        for entry in self.manbyo_dict:
            # 0番目を出現形として使用
            entry.name = self.preprocessor.preprocess(entry.name)[0]

        # load converter
        if isinstance(converter, str):
            if converter == "exact":
                self.converter = exact_matcher.ExactMatchConverter(self.manbyo_dict)
            elif converter == "fuzzy":
                self.converter = fuzzy_matcher.FuzzyMatchConverter(self.manbyo_dict)
            elif converter == "dnorm":
                self.converter = dnorm.dnorm_converter.DNormConverter(self.manbyo_dict)
            assert NotImplementedError, "Please specify converter by selecting (exact|fuzzy|dnorm)"
        elif isinstance(converter, BaseConverter):
            self.converter = converter
        else:
            assert NotImplementedError, "Please specify converter by selecting (exact|fuzzy|dnorm) or creating your own converter inheriting BaseConverter"



    def load_manbyo_dict(self):
        """Load manbyo dict

        This method create cache folder and download the manbyo dictionary.
        You can specify cache folder by setting environment variable "DEFAULT_CACHE_PATH"
        """
        DEFAULT_CACHE_PATH = os.getenv("DEFAULT_CACHE_PATH", "~/.cache")
        DEFAULT_MANBYO_PATH = Path(os.path.expanduser(
                        os.path.join(DEFAULT_CACHE_PATH, "norm")
                ))
        DEFAULT_MANBYO_PATH.mkdir(parents=True, exist_ok=True)

        if not (DEFAULT_MANBYO_PATH / "MANBYO_SABC.csv").exists():
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
        preprocessed_words = self.preprocessor.preprocess(word)
        max_score = -float('inf')
        max_word = None
        for preprocessed_word in preprocessed_words:
            result, sim = self.converter.convert(preprocessed_word)
            if max_word is None or sim > max_score:
                max_score = sim
                max_word = result

        return max_word

