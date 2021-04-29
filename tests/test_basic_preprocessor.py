import pytest

from disease_normalizer.preprocessor.basic_preprocessor import (
    IdenticalPreprocessor,
    FullWidthPreprocessor,
    NFKCPreprocessor,
)

@pytest.mark.parametrize(
    "name, result", [
        ("急性骨髄性白血病", ["急性骨髄性白血病"]),
        ("ajoefijawf", ["ajoefijawf"])
    ]
)
def test_identical_preprocessor(name, result):
    preprocessor = IdenticalPreprocessor()
    output = preprocessor.preprocess(name)
    assert output == result

@pytest.mark.parametrize(
    "name, result", [
        ("123abcｱｲｳ", ["１２３ａｂｃアイウ"]),
        ("Ca欠乏症", ["Ｃａ欠乏症"])
    ]
)
def test_fullwidth_preprocessor(name, result):
    preprocessor = FullWidthPreprocessor()
    output = preprocessor.preprocess(name)
    assert output == result

@pytest.mark.parametrize(
    "name, result", [
        ("今日はいい天気だな〜", ["今日はいい天気だなー"])
    ]
)
def test_NFKC_preprocessor(name, result):
    preprocessor = NFKCPreprocessor()
    output = preprocessor.preprocess(name)
    assert output == result
