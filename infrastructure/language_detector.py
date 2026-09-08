from domain.types import Languages_Used, Difficulty_Level
import langdetect

def detect_language(text: str) -> Languages_Used:
    detected = langdetect.detect(text)

    if detected == 'ru':
        return Languages_Used.RUSSIAN

    elif detected == 'en':
        return Languages_Used.ENGLISH

    elif detected == 'de':
        return Languages_Used.GERMAN

    elif detected == 'fr':
        return Languages_Used.FRANCE
