import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / 'data'

with open(DATA_DIR / 'rareDictEn.json', encoding='utf-8') as f:
    rareDictEn = json.load(f)

with open(DATA_DIR / 'rareDictRu.json', encoding='utf-8') as f:
    rareDictRu = json.load(f)

with open(DATA_DIR / 'rareDictDe.json', encoding='utf-8') as f:
    rareDictDe = json.load(f)

with open(DATA_DIR / 'rareDictFr.json', encoding='utf-8') as f:
    rareDictFr = json.load(f)




