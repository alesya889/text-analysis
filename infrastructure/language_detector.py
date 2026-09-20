from domain.types import Languages_Used, Difficulty_Level
import langdetect

def detectLanguage(text: str) -> Languages_Used:
    """Detects the language of the text"""
    detected = langdetect.detect(text)

    if detected == 'ru':
        return Languages_Used.RUSSIAN

    elif detected == 'en':
        return Languages_Used.ENGLISH

    elif detected == 'de':
        return Languages_Used.GERMAN

    elif detected == 'fr':
        return Languages_Used.FRANCE
    else:
        return Languages_Used.ENGLISH

