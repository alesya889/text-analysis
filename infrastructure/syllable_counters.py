import eng_to_ipa as ipa


def count_syllables_en(word: str) -> int:
    """Count syllables in English word"""

    cnt = 0
    transcription = ipa.convert(word.lower())
    print(transcription)
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

    cnt = 0
    diphthongs_letters = ['ei', 'ai', 'ey', 'ay', 'au', 'eu', 'äu' ]

    for letter in word.lower():
        if letter in diphthongs_letters:
            cnt += 1



