import os

import pytest
from disease_normalizer.normalizer import Normalizer
from disease_normalizer.converter import exact_matcher, fuzzy_matcher, dnorm
from disease_normalizer.converter.base_converter import BaseConverter
from disease_normalizer.utils import DictEntry
from disease_normalizer.preprocessor.basic_preprocessor import (
    FullWidthPreprocessor,
    NFKCPreprocessor,
)
from disease_normalizer.preprocessor.pipeline import PreprocessorPipeline

def test_download_manbyo(tmpdir):
    base_dir = tmpdir.mkdir("norm")
    os.environ["DEFAULT_CACHE_PATH"] = str(base_dir)

    model = Normalizer("basic", "exact")
    assert (base_dir / "norm" / "MANBYO_SABC.csv").exists()
    assert hasattr(model, "manbyo_dict")

def test_manbyo_cache(tmpdir):
    base_dir = tmpdir.mkdir("norm")
    os.environ["DEFAULT_CACHE_PATH"] = str(base_dir)

    model = Normalizer("basic", "exact")
    model = Normalizer("basic", "exact")
    assert hasattr(model, "manbyo_dict")

@pytest.mark.parametrize(
    "name, model", [
    ("exact", exact_matcher.ExactMatchConverter),
    ("fuzzy", fuzzy_matcher.FuzzyMatchConverter),
    ("dnorm", dnorm.dnorm_converter.DNormConverter),
    ("おあいじょふぇ", dnorm.dnorm_converter.DNormConverter),
    ]
)
def test_load_model(name, model, mocker):
    mock_dic = [DictEntry("こんにちは", None, "こんにちは", None) for i in range(10)]
    mocker.patch("disease_normalizer.normalizer.Normalizer.load_manbyo_dict", return_value=mock_dic)

    target_model = Normalizer("basic", name)
    assert type(target_model.converter) == model


def test_load_own_model(mocker):
    class MyConverter(BaseConverter):
        def __init__(self):
            pass

        def convert(self, word):
            return word

    mock_dic = [DictEntry("こんにちは", None, "こんにちは", None) for i in range(10)]
    mocker.patch("disease_normalizer.normalizer.Normalizer.load_manbyo_dict", return_value=mock_dic)

    target_model = Normalizer("basic", MyConverter())
    assert type(target_model.converter) == MyConverter

@pytest.mark.parametrize(
    "name, models", [
        ("basic", [NFKCPreprocessor, FullWidthPreprocessor])
    ]
)
def test_load_predefined_pipeline(name, models, mocker):
    mock_dic = [DictEntry("こんにちは", None, "こんにちは", None) for i in range(10)]
    mocker.patch("disease_normalizer.normalizer.Normalizer.load_manbyo_dict", return_value=mock_dic)

    target_model = Normalizer(name, "exact")
    for pipeline, model in zip(target_model.preprocessor.pipelines, models):
        assert type(pipeline) == model


def test_load_own_pipeline(mocker):
    mock_dic = [DictEntry("こんにちは", None, "こんにちは", None) for i in range(10)]
    mocker.patch("disease_normalizer.normalizer.Normalizer.load_manbyo_dict", return_value=mock_dic)

    mypipeline = PreprocessorPipeline(['identical'])

    target_model = Normalizer(mypipeline, "exact")
    assert type(target_model.preprocessor) == PreprocessorPipeline


@pytest.mark.parametrize(
    "input, converter_name, preprocessor_name, output", [
        ("2型糖尿病", "exact", "basic", DictEntry("２型糖尿病", "E11", "２型糖尿病", "S"))
    ]
)
def test_normalize(input, converter_name, preprocessor_name, output, manbyo_dict, mocker):
    mocker.patch("disease_normalizer.normalizer.Normalizer.load_manbyo_dict", return_value=manbyo_dict)

    target_model = Normalizer(preprocessor_name, converter_name)
    result = target_model.normalize(input)
    assert result.icd == output.icd
    assert result.norm == output.norm
