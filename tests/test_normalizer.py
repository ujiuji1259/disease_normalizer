import os

import pytest
from disease_normalizer.normalizer import Normalizer
from disease_normalizer.converter import exact_matcher, fuzzy_matcher, dnorm

def test_download_manbyo(tmpdir):
    base_dir = tmpdir.mkdir("norm")
    os.environ["DEFAULT_CACHE_PATH"] = str(base_dir)

    model = Normalizer(None, "exact")
    assert (base_dir / "norm" / "MANBYO_SABC.csv").exists()
    assert hasattr(model, "manbyo_dict")

def test_manbyo_cache(tmpdir):
    base_dir = tmpdir.mkdir("norm")
    os.environ["DEFAULT_CACHE_PATH"] = str(base_dir)

    model = Normalizer(None, "exact")
    model = Normalizer(None, "exact")
    assert hasattr(model, "manbyo_dict")

@pytest.mark.parametrize(
    "name, model", [
    ("exact", exact_matcher.ExactMatchConverter),
    ("fuzzy", fuzzy_matcher.FuzzyMatchConverter),
    ("dnorm", dnorm.dnorm_converter.DNormConverter),
    ("おあいじょふぇ", dnorm.dnorm_converter.DNormConverter),
    ]
)
def test_load_model(name, model, tmpdir):
    base_dir = tmpdir.mkdir("norm")
    os.environ["DEFAULT_CACHE_PATH"] = str(base_dir)

    target_model = Normalizer(None, name)
    assert type(target_model.converter) == model

