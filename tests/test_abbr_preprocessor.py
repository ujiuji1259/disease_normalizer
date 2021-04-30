
import os

import pytest
from japanese_disease_normalizer.preprocessor.abbr_preprocessor import AbbrPreprocessor, AbbrEntry

def test_download_abbr_dict(tmpdir, monkeypatch):
    base_dir = tmpdir.mkdir("norm")
    monkeypatch.setenv("DEFAULT_CACHE_PATH", str(base_dir))

    model = AbbrPreprocessor()
    assert (base_dir / "norm" / "abb_dict.json").exists()
    assert isinstance(model.abbr_dict, dict)
    assert isinstance(model.abbr_dict[list(model.abbr_dict.keys())[0]], list)
    assert isinstance(model.abbr_dict[list(model.abbr_dict.keys())[0]][0], AbbrEntry)

def test_load_abbr_already_downloaded(tmpdir, manbyo_dict, monkeypatch):
    base_dir = tmpdir.mkdir("norm")
    monkeypatch.setenv("DEFAULT_CACHE_PATH", str(base_dir))

    model = AbbrPreprocessor()
    model = AbbrPreprocessor()
    assert (base_dir / "norm" / "abb_dict.json").exists()
    assert isinstance(model.abbr_dict, dict)
    assert isinstance(model.abbr_dict[list(model.abbr_dict.keys())[0]], list)
    assert isinstance(model.abbr_dict[list(model.abbr_dict.keys())[0]][0], AbbrEntry)


@pytest.mark.parametrize(
    "input, outputs", [
        ("Kだよー", ["Kだよー", "カリウムだよー", "角化上皮だよー", "クレブシエラ属だよー"]),
        ("Ｋだよー", ["Kだよー", "カリウムだよー", "角化上皮だよー", "クレブシエラ属だよー"]),
        ("わいわいACL", ["わいわいACL", "わいわい前十字靱帯", "わいわいアルブミン カゼイン レシチン"]),
        ("わいわい    ACL  ", ["わいわい    ACL", "わいわい    前十字靱帯", "わいわい    アルブミン カゼイン レシチン"]),
        ("KのACLなんじゃ", [
            "KのACLなんじゃ", "Kの前十字靱帯なんじゃ", "Kのアルブミン カゼイン レシチンなんじゃ",
            "カリウムのACLなんじゃ", "カリウムの前十字靱帯なんじゃ", "カリウムのアルブミン カゼイン レシチンなんじゃ",
            "角化上皮のACLなんじゃ", "角化上皮の前十字靱帯なんじゃ", "角化上皮のアルブミン カゼイン レシチンなんじゃ",
            "クレブシエラ属のACLなんじゃ", "クレブシエラ属の前十字靱帯なんじゃ", "クレブシエラ属のアルブミン カゼイン レシチンなんじゃ"])
    ]
)
def test_preprocess(input, outputs, tmpdir, monkeypatch):
    base_dir = tmpdir.mkdir("norm")
    monkeypatch.setenv("DEFAULT_CACHE_PATH", str(base_dir))

    model = AbbrPreprocessor()
    results = model.preprocess(input)
    assert len(results) == len(outputs)
    results.sort()
    outputs.sort()
    for result, output in zip(results, outputs):
        assert result == output
