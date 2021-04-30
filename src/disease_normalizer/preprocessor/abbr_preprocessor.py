import os
import re
import json
from pathlib import Path
from dataclasses import dataclass

import jaconv
from .base_preprocessor import BasePreprocessor
from .. import utils

BASE_URL = "http://aoi.naist.jp/norm/abb_dic.json"


@dataclass
class AbbrEntry:
    abbr: str
    name: str
    freq: int


class AbbrPreprocessor(BasePreprocessor):
    def __init__(self):
        self.abbr_dict = self.load_abbr_dict()

    def preprocess(self, word):
        word = jaconv.z2h(word, kana=False, ascii=True, digit=True)
        iters = re.finditer(r'([a-zA-Z][a-zA-Z\s]*)', word)

        pos = 0
        output_words = []
        for ite in iters:
            s_pos, e_pos = ite.span()
            abbr = ite.groups()[0].strip()

            if pos != s_pos:
                output_words.append(word[pos:s_pos])

            s_word = [abbr]
            if abbr in self.abbr_dict:
                s_word += [w.name for w in self.abbr_dict[abbr]]
            elif word.lower() in self.abbr_dict:
                s_word += [w.name for w in self.abbr_dict[abbr.lower()]]

            output_words.append(s_word)
            pos = e_pos

        output_words.append(word[pos:])

        def flatten_words(word_list):
            if len(word_list) == 0:
                return [[]]

            if isinstance(word_list[0], str):
                results = [[word_list[0]] + l for l in flatten_words(word_list[1:])]
            elif isinstance(word_list[0], list):
                results = [[w] + l for w in word_list[0] for l in flatten_words(word_list[1:])]
            return results

        results = flatten_words(output_words)
        results = [''.join(l) for l in results]
        #results = [jaconv.h2z(r, kana=True, digit=True, ascii=True) for r in results]

        return results

    def load_abbr_dict(self):
        DEFAULT_CACHE_PATH = os.getenv("DEFAULT_CACHE_PATH", "~/.cache")
        DEFAULT_ABBR_PATH = Path(os.path.expanduser(
                os.path.join(DEFAULT_CACHE_PATH, "norm")
        ))
        DEFAULT_ABBR_PATH.mkdir(parents=True, exist_ok=True)

        if not (DEFAULT_ABBR_PATH / "abb_dict.json").exists():
            utils.download_fileobj(BASE_URL, DEFAULT_ABBR_PATH / "abb_dict.json")

        with open(DEFAULT_ABBR_PATH / "abb_dict.json", 'r') as f:
            abbr_dict = json.load(f)

        results = {key: [AbbrEntry(key, v[1], v[0]) for v in abbr_dict[key]] for key in abbr_dict.keys()}
        return results
