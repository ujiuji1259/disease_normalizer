import pytest
from disease_normalizer.utils import load_dict

def test_load_dict():
    dict_entries = load_dict("tests/sample_dict.csv")
    for d in dict_entries:
        assert isinstance(d.name, str)
        assert isinstance(d.icd, str)
        assert isinstance(d.norm, str)
        assert d.level in ["S", "A", "B", "C"]
