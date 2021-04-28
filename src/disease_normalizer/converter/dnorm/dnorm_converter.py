import os
from pathlib import Path

from .dnorm import DNorm
from ... import utils



BASE_URL = "http://aoi.naist.jp/DNorm/dnorm.pkl"


class DNormConverter(object):
    def __init__(self, dictionary):
        self.dict = {d.name: d for d in dictionary}
        self.build_model(dictionary)

    def convert(self, word):
        result = self.model.predict([word], k=1)[0][0]
        return self.dict[result]

    def build_model(self, dictionary):
        DEFAULT_CACHE_PATH = os.getenv("DEFAULT_CACHE_PATH", "~/.cache")
        DEFAULT_DNORM_PATH = Path(os.path.expanduser(
                os.path.join(DEFAULT_CACHE_PATH, "Dnorm")
        ))
        DEFAULT_DNORM_PATH.mkdir(parents=True, exist_ok=True)

        if not (DEFAULT_DNORM_PATH / "dnorm.pkl").exists():
            utils.download_fileobj(BASE_URL, DEFAULT_DNORM_PATH / "dnorm.pkl")

        self.model = DNorm(dictionary, DEFAULT_DNORM_PATH / "dnorm.pkl")
