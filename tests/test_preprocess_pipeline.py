import pytest

from disease_normalizer.preprocessor.basic_preprocessor import BasePreprocessor
from disease_normalizer.preprocessor.basic_preprocessor import (
    FullWidthPreprocessor,
    NFKCPreprocessor,
    IdenticalPreprocessor
)
from disease_normalizer.preprocessor.pipeline import PreprocessorPipeline

@pytest.mark.parametrize(
    "pipelines, models", [
        (["fullwidth", "NFKC"], [FullWidthPreprocessor, NFKCPreprocessor]),
        (["identical", "NFKC"], [IdenticalPreprocessor, NFKCPreprocessor]),
    ]
)
def test_load_preprocessor_from_predefined(pipelines, models):
    model = PreprocessorPipeline(pipelines)
    for preprocessor, model in zip(model.pipelines, models):
        assert type(preprocessor) == model

@pytest.mark.parametrize(
    "pipelines, models", [
        ([], []),
        (["fullwidth", "NFKC"], [FullWidthPreprocessor, NFKCPreprocessor]),
        (["identical", "NFKC"], [IdenticalPreprocessor, NFKCPreprocessor]),
    ]
)
def test_load_preprocessor_from_own(pipelines, models):
    class MyPreprocessor(BasePreprocessor):
        def __init__(self):
            pass

        def preprocess(self, word):
            return [word]

    my_preprocessor = MyPreprocessor()
    pipelines.append(my_preprocessor)
    models.append(MyPreprocessor)

    model = PreprocessorPipeline(pipelines)
    for preprocessor, model in zip(model.pipelines, models):
        assert type(preprocessor) == model


@pytest.mark.parametrize(
    "input, pipelines, outputs", [
        ("ｺﾝﾆﾁﾊ〜", ["identical"], ["ｺﾝﾆﾁﾊ〜"]),
        ("ｺﾝﾆﾁﾊ〜", ["fullwidth"], ["コンニチハ〜"]),
        ("ｺﾝﾆﾁﾊ〜", ["NFKC"], ["コンニチハー"]),
        ("ｺﾝﾆﾁﾊ〜", ["NFKC", "fullwidth"], ["コンニチハー"]),
        ("2型糖尿病", ["NFKC", "fullwidth"], ["２型糖尿病"]),
    ]
)
def test_preprocess(input, pipelines, outputs):
    model = PreprocessorPipeline(pipelines)
    results = model.preprocess(input)
    outputs.sort()
    results.sort()
    for output, result in zip(outputs, results):
        assert output == result
