"""Set of utility functions
"""

import csv
from dataclasses import dataclass

@dataclass
class DictEntry:
    """Entry of manbyo dictionary

    attributes:
        name: surface form of the disease
        icd: icd-10 code
        norm: normalized form of the disease
        level: confidence level in the manbyo dictionary
    """
    name: str
    icd: str
    norm: str
    level: str

def load_dict(path):
    """Load manbyo dictionary

    args:
        path: str

    return:
        data: List[DictEntry]
    """
    data = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(DictEntry(*row))
    return data