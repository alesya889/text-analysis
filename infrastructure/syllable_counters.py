import eng_to_ipa as ipa
import pyphen




def count_syllables_en(word: str) -> int:
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

def count_syllables_ru(word: str) -> int:
    """Count syllables in Russian word"""

    vowels = ['а', 'о', 'е', "ё" , "у", 'ы', 'и', 'я', "ю" , "э"]
    cnt = 0

    for letter in word.lower():
        if letter in vowels:
            cnt += 1

    return cnt

def count_syllables_ge(word: str) -> int:
    """Count syllables in German word"""

    dic = pyphen.Pyphen(lang='de_DE')
    hyphenated = dic.inserted(word)
    return hyphenated.count('-') + 1

def count_syllables_fr(word: str) -> int:
    """Count syllables in French word"""

    dic = pyphen.Pyphen(lang='fr_FR')
    hyphenated = dic.inserted(word)
    return hyphenated.count('-') + 1






