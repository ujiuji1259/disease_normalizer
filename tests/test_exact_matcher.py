import pytest
from japanese_disease_normalizer.converter.exact_matcher import ExactMatchConverter

@pytest.mark.parametrize(
    "name, icd, norm", [
    ("疼痛", "R529", "疼痛"),
    ("頭痛だ", None, None)]
)
def test_exact_match(name, icd, norm, manbyo_dict):
    converter = ExactMatchConverter(manbyo_dict)
    result, sim = converter.convert(name)
    assert result.icd == icd
    assert result.norm == norm
