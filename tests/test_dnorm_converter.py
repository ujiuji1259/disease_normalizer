import os

import pytest
from japanese_disease_normalizer.converter.dnorm.dnorm_converter import DNormConverter

def test_download_model(tmpdir, manbyo_dict, monkeypatch):
    base_dir = tmpdir.mkdir("dnorm")
    monkeypatch.setenv("DEFAULT_CACHE_PATH", str(base_dir))

    model = DNormConverter(manbyo_dict)
    assert (base_dir / "Dnorm" / "dnorm.pkl").exists()
    assert hasattr(model.model, "tfidf")
    assert hasattr(model.model, "W")

def test_load_model_already_downloaded(tmpdir, manbyo_dict, monkeypatch):
    base_dir = tmpdir.mkdir("dnorm")
    monkeypatch.setenv("DEFAULT_CACHE_PATH", str(base_dir))

    model = DNormConverter(manbyo_dict)
    model = DNormConverter(manbyo_dict)
    assert hasattr(model.model, "tfidf")
    assert hasattr(model.model, "W")

@pytest.mark.parametrize(
    "name, icd, norm", [
    ("疼痛", "R529", "疼痛"),
    ("頭痛だ", "R51", "頭痛"),
    ("悪性リンパ腫だよおおおおお", "C859", "悪性リンパ腫"),
    ]
)
def test_dnorm_match(name, icd, norm, manbyo_dict, tmpdir, monkeypatch):
    base_dir = tmpdir.mkdir("dnorm")
    monkeypatch.setenv("DEFAULT_CACHE_PATH", str(base_dir))

    converter = DNormConverter(manbyo_dict)

    result, sim = converter.convert(name)

    assert result.icd == icd
    assert result.norm == norm
