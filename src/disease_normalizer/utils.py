import csv
from dataclasses import dataclass

@dataclass
class DictEntry:
    name: str
    icd: str
    norm: str
    level: str

def load_dict(path):
    data = []
    with open(path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(DictEntry(*row))
    return data