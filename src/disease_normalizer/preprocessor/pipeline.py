"""Pipeline of preprocessor

This module merge some preprocessor into one pipeline system.
"""

from .base_preprocessor import BasePreprocessor
from .abbr_preprocessor import AbbrPreprocessor
from .basic_preprocessor import (
    IdenticalPreprocessor,
    FullWidthPreprocessor,
    NFKCPreprocessor,
)

class PreprocessorPipeline(object):
    """Pipeline of preprocessor

    You can create pipeline of preprocessor using pre-defined preprocessor (identical|fullwidth|NFKC|abbr)
    or your own preprocessor inherited BasePreprocessor.

    Args:
        preprocessors List[Union[str, BasePreprocessor]]: list of preprocessor
    """
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
        """Perform all preprocess

        This method return the list of preprocessed string because some preprocessor could return more than one string because of the ambiguity (e.g. AbbrPreprocessor).

        Args:
            word str: disease name

        Returns:
            List[str]: all preprocessed disease names
        """
        results = [word]
        for preprocessor in self.pipelines:
            results = [preprocessor.preprocess(w) for w in results]
            results = [w for ww in results for w in ww]

        return results
