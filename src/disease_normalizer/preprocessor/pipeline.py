from .base_preprocessor import BasePreprocessor
from .abbr_preprocessor import AbbrPreprocessor
from .basic_preprocessor import (
    IdenticalPreprocessor,
    FullWidthPreprocessor,
    NFKCPreprocessor,
)

class PreprocessorPipeline(object):
    def __init__(self, preprocessors):
        self.pipelines = []

        for preprocessor in preprocessors:
            if isinstance(preprocessor, BasePreprocessor):
                self.pipelines.append(preprocessor)
            elif isinstance(preprocessor, str):
                if preprocessor == "identical":
                    self.pipelines.append(IdenticalPreprocessor())
                elif preprocessor == "fullwidth":
                    self.pipelines.append(FullWidthPreprocessor())
                elif preprocessor == "NFKC":
                    self.pipelines.append(NFKCPreprocessor())
                elif preprocessor == "abbr":
                    self.pipelines.append(AbbrPreprocessor())
                else:
                    assert NotImplementedError, "If you want to use pre-defined preprocessor, please select one from (identical|fullwidth|NFKC)"
            else:
                assert NotImplementedError, "Please specify str or BasePreprocessor instance"

    def preprocess(self, word):
        results = [word]
        for preprocessor in self.pipelines:
            results = [preprocessor.preprocess(w) for w in results]
            results = [w for ww in results for w in ww]

        return results
