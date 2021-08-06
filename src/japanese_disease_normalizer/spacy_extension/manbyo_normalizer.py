try:
    from spacy.language import Language
    from spacy.tokens import Doc, Span
except:
    raise NotImplementedError("Spacy is not installed")

from japanese_disease_normalizer.normalizer import Normalizer

@Language.factory("manbyo_normalizer")
class ManbyoNormalizer:
    def __init__(self, nlp, name):
        self.normalizer = Normalizer("abbr", "fuzzy")
        Span.set_extension("norm", default=None)

    def __call__(self, doc):
        for ent in doc.ents:
            entity = ent.text
            norm = self.normalizer.normalize(entity)
            ent._.set("norm", norm)
        return doc

    def to_disk(self, path, exclude=tuple()):
        pass

    def from_disk(self, path, exclude=tuple()):
        return self
