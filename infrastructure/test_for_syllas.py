import syllabreak
word = 'haus'
diphthongs = ['ae', 'ao', 'oø']
    monophthongs = ['aː', 'a', 'eː', 'e', 'iː', 'i', 'oː', 'o', 'uː', 'u', 'ɛː', 'ɛ', 'øː', 'œ', 'aː', 'a', 'ɔː', 'ɒ']

    for sound in diphthongs:
        if sound in transcription:
            cnt += 1
            transcription = transcription.replace(sound, '', 1)

    for sound in transcription:
        if sound in monophthongs:
            cnt += 1
print(syllabreak(word, lang='de'))