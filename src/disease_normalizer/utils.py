"""Set of utility functions
"""

import csv
import shutil
import requests
from dataclasses import dataclass

@dataclass
class DictEntry:
    """Entry of manbyo dictionary

    attributes:
        name str: surface form of the disease
        icd str: icd-10 code
        norm str: normalized form of the disease
        level str: confidence level in the manbyo dictionary
    """
    name: str
    icd: str
    norm: str
    level: str

def load_dict(path):
    """Load manbyo dictionary

    args:
        path str: path of the manbyo dictionary

    return:
        data List[DictEntry]: disease list in the manbyo dictionary
    """
    data = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(DictEntry(*row))
    return data

def download_fileobj(src, dst, binary=False):
    """Download files from url

    Args:
        src str: url from which you want to download
        dst str: path where you save the file
        binary bool: whether the file is binary or not
    """
    res = requests.get(src, stream=True)
    with open(dst, "wb") as f:
        shutil.copyfileobj(res.raw, f)