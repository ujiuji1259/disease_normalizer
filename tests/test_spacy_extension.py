import pytest
from spacy.tokens import Span
from spacy.lang.ja import Japanese

from japanese_disease_normalizer.spacy_extension.manbyo_normalizer import ManbyoNormalizer
from japanese_disease_normalizer.utils import DictEntry

def test_manbyo_normalizer():
    nlp = Japanese(meta={"tokenizer": {"config": {"split_mode": "B"}}})
    component = ManbyoNormalizer(None, None)

    true_entry = DictEntry("急性骨髄性白血病", "C920", norm="急性骨髄性白血病", level="S")

    doc = nlp("急性骨髄性白血病にて緊急入院")
    doc.set_ents([Span(doc, 0, 5, "C")])
    doc = component(doc)
    for ent in doc.ents:
        norm = ent._.norm
        assert norm.icd == true_entry.icd
        assert norm.norm == true_entry.norm
        assert norm.level == true_entry.level

    doc = nlp("急性骨髄白血にて緊急入院")
    doc.set_ents([Span(doc, 0, 3, "C")])
    doc = component(doc)
    for ent in doc.ents:
        norm = ent._.norm
        assert norm.icd == true_entry.icd
        assert norm.norm == true_entry.norm
        assert norm.level == true_entry.level
