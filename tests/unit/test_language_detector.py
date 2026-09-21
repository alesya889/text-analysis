from domain.types import Languages_Used
from infrastructure.language_detector import detectLanguage


def test_detect_russian():
    # Проверяет определение русского языка.
    assert detectLanguage("Привет, как дела? Мы друзья?") == Languages_Used.RUSSIAN


def test_detect_english():
    # Проверяет определение английского языка.
    assert detectLanguage("Hello, how are you?") == Languages_Used.ENGLISH


def test_detect_german():
    # Проверяет определение немецкого языка.
    assert detectLanguage("Hallo, wie geht es dir?") == Languages_Used.GERMAN


def test_detect_french():
    # Проверяет определение французского языка.
    assert detectLanguage("Bonjour, comment ça va?") == Languages_Used.FRANCE


def test_detect_unrecognized_language():
    # Проверяет определение нераспознанного языка (по умолчанию английский).
    assert detectLanguage("你好，世界") == Languages_Used.ENGLISH
