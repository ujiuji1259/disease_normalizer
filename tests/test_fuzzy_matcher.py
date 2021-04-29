import pytest
from disease_normalizer.converter.fuzzy_matcher import FuzzyMatchConverter

@pytest.mark.parametrize(
    "name, icd, norm", [
    ("疼痛", "R529", "疼痛"),
    ("頭痛だ", "R51", "頭痛"),
    ("aobijosdf", None, None),
    ]
)
def test_fuzzy_match(name, icd, norm, manbyo_dict):
    converter = FuzzyMatchConverter(manbyo_dict)
    result, sim = converter.convert(name)
    assert result.icd == icd, result.icd
    assert result.norm == norm, result.norm
