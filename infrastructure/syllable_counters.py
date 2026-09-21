import eng_to_ipa as ipa
import pyphen
from domain.types import Languages_Used
from domain.interfaces import SyllableCounter


def countSyllablesEn(word: str) -> int:
    # Cчитает слоги для английского

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
    # Cчитает слоги для русского

    vowels = ['а', 'о', 'е', "ё" , "у", 'ы', 'и', 'я', "ю" , "э"]
    cnt = 0

    for letter in word.lower():
        if letter in vowels:
            cnt += 1

    return cnt

def countSyllablesGe(word: str) -> int:
    # Cчитает слоги для немецкого

    dic = pyphen.Pyphen(lang='de_DE')
    hyphenated = dic.inserted(word)
    return hyphenated.count('-') + 1 if len(word) > 0 else 0

def countSyllablesFr(word: str) -> int:
    # Считает слоги для французского
    dic = pyphen.Pyphen(lang='fr_FR')
    hyphenated = dic.inserted(word)
    return hyphenated.count('-') + 1 if len(word) > 0 else 0

def getSyllableCounter(lang: Languages_Used) -> SyllableCounter:
    # Определяет, какую функцию надо использовать для подсчета слогов в зависимости от языка
    if lang == Languages_Used.ENGLISH:
        return countSyllablesEn
    elif lang == Languages_Used.RUSSIAN:
        return countSyllablesRu
    elif lang == Languages_Used.GERMAN:
        return countSyllablesGe
    elif lang == Languages_Used.FRANCE:
        return countSyllablesFr
    else:
        raise ValueError(f"Unsupported language: {lang}")