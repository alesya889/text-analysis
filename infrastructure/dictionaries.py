import json
from pathlib import Path
from ruword_frequency import Frequency
from wordfreq import get_frequency_dict, zipf_frequency, iter_wordlist

rareDictRu = {}
BARRIER_RU = 5.0
freq = Frequency()
freq.load()
rare_words_set = set()
for word in freq.iterate_words(0.0):
    if freq.ipm(word) < BARRIER_RU:
        rare_words_set.add(word)
for word in rare_words_set:
    rareDictRu[word] = freq.ipm(word)

all_freqs_en = get_frequency_dict('en')
all_freqs_de = get_frequency_dict('de')
all_freqs_fr = get_frequency_dict('fr')
rareDictEn = {}
rareDictDe = {}
rareDictFr = {}

for word, freq in all_freqs_en.items():
    zipf = zipf_frequency(word, 'en')
    if zipf < 2.0:
        rareDictEn[word] = zipf

for word, freq in all_freqs_de.items():
    zipf = zipf_frequency(word, 'de')
    if zipf < 2.0:
        rareDictDe[word] = zipf

for word, freq in all_freqs_fr.items():
    zipf = zipf_frequency(word, 'fr')
    if zipf < 2.0:
        rareDictFr[word] = zipf
