import pytest
from application.use_cases import (
    splitSentences, splitWords, lexicalDiversity, validateText,
    computeStats, fleschIndex, analyzeTextService,
)
from domain.types import Languages_Used, Polarity, TextStats

def test_splitSentences_simple():
    result = splitSentences("Привет мир. Как дела?")
    assert len(result) == 2

def test_splitSentences_hard():
    result = splitSentences("Привет!! Ты мне очень дорог . что думаешь?!")
    assert len(result) == 3

def test_splitSentences_empty():
    result = splitSentences("")
    assert len(result) == 0

def test_splitSentences_without_punctuation():
    result = splitSentences("Привет как дела")
    assert len(result) == 1

def test_splitWords():
    result = splitWords("Привет, мир!")
    assert result == ["Привет", "мир"]

def test_splitWords_empty():
    result = splitWords("")
    assert result == []

def test_splitWords_apostrophe():
    result = splitWords("I don't like you.")
    assert result == ["I", "don't", "like", "you"]

def test_lexicalDiversity_unique():
    assert lexicalDiversity("мама мыла раму") == 1.0

def test_lexicalDiversity_repeats():
    assert lexicalDiversity("мама мыла раму мама") == 0.75

def test_validateText_empty():
    with pytest.raises(ValueError):
        validateText("")

def test_validateText_valid():
    validateText("Привет мир!")

def fake_detector(text: str) -> Languages_Used:
    return Languages_Used.RUSSIAN

def fake_counter(word: str) -> int:
    return 2

def fake_sentiment(text: str) -> tuple[Polarity, float]:
    return Polarity.Positive, 0.8


def test_analyzeTextService_returns_result():
    result = analyzeTextService(
        "Привет мир. Как дела?",
        fake_detector,  # ← всегда RUSSIAN
        fake_counter,  # ← всегда 2 слога
        fake_sentiment,  # ← всегда POSITIVE, 0.8
    )

    assert result.language == Languages_Used.RUSSIAN  # ← заглушка сработала
    assert result.polarity == Polarity.Positive# ← заглушка сработала
    assert result.subjectivity == 0.8  # ← заглушка сработала
    assert result.stats.word_count == 4  # ← реальная логика splitWords
    assert result.stats.syllable_count == 8

def test_analyzeTextService_empty_raises():
    with pytest.raises(ValueError):
        analyzeTextService(
            "",
            fake_detector,
            fake_counter,
            fake_sentiment,
        )

def test_analyzeTextService_invalid_chars_raises():
    with pytest.raises(ValueError):
        analyzeTextService(
            "Привет 😀 мир!",
            fake_detector,
            fake_counter,
            fake_sentiment,
        )