"""Fuzzy match using DNorm

DNorm is the disease normalization model based on the ranking model with tf-idf vector.
"""
import os
from pathlib import Path

from .dnorm import DNorm
from ... import utils



BASE_URL = "http://aoi.naist.jp/DNorm/dnorm.pkl"


class DNormConverter(object):
    """DNorm converter

    Args:
        dictionary List[DictEntry]: manbyo dictionary

    Attributes:
        dict Dict[str: DictEntry]: manbyo dictionary
        model DNorm: DNorm model
    """
    def __init__(self, dictionary):
        self.dict = {d.name: d for d in dictionary}
        self.build_model(dictionary)

    def convert(self, word):
        """Convert surface form of the disease into the normalized form.

        Args:
            word str: surface form of the disease

        Returns:
            DictEntry: DictEntry of normalized form of the disease
        """
        result = self.model.predict([word], k=1)[0][0]
        return self.dict[result]

    def build_model(self, dictionary):
        """Build dnorm

        Load dnorm model from ~/.cache/Dnorm/dnorm.pkl if the path exists.
        Otherwise, automatically download the dnorm file from remote-url.
        You can specify the cache directory by setting the environment variable "DEFAULT_CACHE_PATH"

        Args:
            dictionary List[DictEntry]: manbyo dictionary

        """
        DEFAULT_CACHE_PATH = os.getenv("DEFAULT_CACHE_PATH", "~/.cache")
        DEFAULT_DNORM_PATH = Path(os.path.expanduser(
                os.path.join(DEFAULT_CACHE_PATH, "Dnorm")
        ))
        DEFAULT_DNORM_PATH.mkdir(parents=True, exist_ok=True)

        if not (DEFAULT_DNORM_PATH / "dnorm.pkl").exists():
            utils.download_fileobj(BASE_URL, DEFAULT_DNORM_PATH / "dnorm.pkl")

        self.model = DNorm(dictionary, DEFAULT_DNORM_PATH / "dnorm.pkl")
