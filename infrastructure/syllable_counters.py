from domain.types import Languages_Used
from domain.interfaces import SyllableCounter
import eng_to_ipa as ipa
import pyphen



def countSyllablesEn(word: str) -> int:
    """Count syllables in English word"""

    cnt = 0
    transcription = ipa.convert(word.lower())
    monophthongs = ['ɪ', 'e', 'æ', 'ʌ', 'ʊ', 'ɒ', 'ə', 'iː', 'ɑː', 'ɔː', 'uː', 'ɜː', 'ɔ', 'ɑ', 'ɛ', 'i']
    diphthongs = ['eɪ', 'aɪ', 'ɔɪ', 'əʊ', 'aʊ', 'ɪə', 'eə', 'ʊə', 'ju', 'oʊ']

    for sound in diphthongs:
        if sound in transcription:
            cnt += 1
            transcription = transcription.replace(sound, '', 1)

    for sound in transcription:
        if sound in monophthongs:
            cnt += 1

    return cnt


def countSyllablesRu(word: str) -> int:
    """Count syllables in Russian word"""

    vowels = ['а', 'о', 'е', "ё" , "у", 'ы', 'и', 'я', "ю" , "э"]
    cnt = 0

    for letter in word.lower():
        if letter in vowels:
            cnt += 1

    return cnt


def countSyllablesGe(word: str) -> int:
    """Count syllables in German word"""

    dic = pyphen.Pyphen(lang='de_DE')
    hyphenated = dic.inserted(word)
    return hyphenated.count('-') + 1

def countSyllablesFr(word: str) -> int:
    """Count syllables in French word"""

    dic = pyphen.Pyphen(lang='fr_FR')
    hyphenated = dic.inserted(word)
    return hyphenated.count('-') + 1


def getSyllableCounter(lang: Languages_Used) -> SyllableCounter:
    if lang == Languages_Used.ENGLISH:
        return countSyllablesEn
    elif lang == Languages_Used.RUSSIAN:
        return countSyllablesRu
    elif lang == Languages_Used.GERMAN:
        return countSyllablesGe
    elif lang == Languages_Used.FRANCE:
        return countSyllablesFr





