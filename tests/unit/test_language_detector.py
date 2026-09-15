from infrastructure.language_detector import detectLanguage
from domain.types import Languages_Used

def test_detect_russian():
    assert detectLanguage("Привет, как дела? Мы друзья?") == Languages_Used.RUSSIAN

def test_detect_english():
    assert detectLanguage("Hello, how are you?") == Languages_Used.ENGLISH

def test_detect_german():
    assert detectLanguage("Hallo, wie geht es dir?") == Languages_Used.GERMAN

def test_detect_french():
    assert detectLanguage("Bonjour, comment ça va?") == Languages_Used.FRANCE

def test_detect_unrecognized_language():
    assert detectLanguage("你好，世界") == Languages_Used.ENGLISH