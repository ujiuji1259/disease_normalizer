import sys
import os

import pytest

sys.path.append(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../src/"))

from japanese_disease_normalizer.utils import load_dict

@pytest.fixture
def manbyo_dict():
    return load_dict("tests/sample_dict.csv")
