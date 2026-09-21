import pytest
from unittest.mock import patch
from application.use_cases import (
  splitSentences, splitWords, lexicalDiversity, validateText, rareWordDensity,
  computeStats, fleschIndex, analyzeTextService, interpretFlesch, analyzeBatchService
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


def test_lexicalDiversity_empty():
  assert lexicalDiversity("") == 0.0


def test_validateText_empty():
  with pytest.raises(ValueError):
    validateText("")


def test_validateText_valid():
  validateText("Привет мир!")


def test_validateText_only_spaces():
  with pytest.raises(ValueError):
    validateText("   ")


def test_validateText_too_long():
  with pytest.raises(ValueError):
    validateText("a" * 200_000)


def test_validateText_no_letters():
  with pytest.raises(ValueError):
    validateText("12345")


def fake_detector(text: str) -> Languages_Used:
  return Languages_Used.RUSSIAN


def fake_counter(word: str) -> int:
  return 2  # ← вернуть определение


def fake_sentiment(text: str) -> tuple[Polarity, float]:
  return Polarity.Positive, 0.8


def test_computeStats_simple():
  stats = computeStats("мама мыла", fake_counter)
  assert stats.sentence_count == 1
  assert stats.word_count == 2
  assert stats.syllable_count == 4
  assert stats.avg_sentence_length == 2.0
  assert stats.avg_word_syllables == 2.0


def test_computeStats_two_sentences():
  stats = computeStats("Привет мир. Как дела?", fake_counter)
  assert stats.sentence_count == 2
  assert stats.word_count == 4
  assert stats.syllable_count == 8


def test_computeStats_empty():
  stats = computeStats("", fake_counter)
  assert stats.word_count == 0
  assert stats.avg_sentence_length == 0
  assert stats.avg_word_syllables == 0


def test_interpretFlesch_english_very_easy():
  assert interpretFlesch(95, Languages_Used.ENGLISH) == "very_easy"


def test_interpretFlesch_english_easy():
  assert interpretFlesch(75, Languages_Used.ENGLISH) == "easy"


def test_interpretFlesch_english_hard():
  assert interpretFlesch(45, Languages_Used.ENGLISH) == "hard"


def test_interpretFlesch_english_very_hard():
  assert interpretFlesch(15, Languages_Used.ENGLISH) == "very_hard"


def test_interpretFlesch_russian_very_easy():
  assert interpretFlesch(85, Languages_Used.RUSSIAN) == "very_easy"


def test_interpretFlesch_clamping_high():
  assert interpretFlesch(150, Languages_Used.ENGLISH) == "very_easy"


def test_interpretFlesch_clamping_low():
  assert interpretFlesch(-50, Languages_Used.ENGLISH) == "very_hard"


def test_rareWordDensity_all_rare():
  freq_dict = {"привет": 1.0, "мир": 1.5}
  assert rareWordDensity("привет мир", freq_dict) == 1.0


def test_rareWordDensity_partial():
  freq_dict = {"привет": 1.0}
  assert rareWordDensity("привет мир", freq_dict) == 0.5


def test_rareWordDensity_empty():
  assert rareWordDensity("", {}) == 0.0


@patch('application.use_cases.getSyllableCounter')
def test_analyzeTextService_returns_result(mock_get_counter):
  mock_get_counter.return_value = fake_counter

  result = analyzeTextService(
    "Привет мир. Как дела?",
    fake_detector,
    fake_sentiment,
  )

  assert result.language == Languages_Used.RUSSIAN
  assert result.polarity == Polarity.Positive
  assert result.subjectivity == 0.8
  assert result.stats.word_count == 4
  assert result.stats.syllable_count == 8


def test_analyzeTextService_empty_raises():
  with pytest.raises(ValueError):
    analyzeTextService(
      "",
      fake_detector,
      fake_sentiment,
    )


def test_analyzeTextService_invalid_chars_raises():
  with pytest.raises(ValueError):
    analyzeTextService(
      "Привет 😀 мир!",
      fake_detector,
      fake_sentiment,
    )


def test_analyzeBatchService_returns_list():
  with patch('application.use_cases.getSyllableCounter') as mock:
    mock.return_value = fake_counter
    results = analyzeBatchService(
      ["Привет мир.", "Hello world."],
      langDetector=fake_detector,
      sentimentAnalyzer=fake_sentiment,
    )
    assert len(results) == 2


def test_analyzeBatchService_empty():
  results = analyzeBatchService(
    [],
    langDetector=fake_detector,
    sentimentAnalyzer=fake_sentiment,
  )
  assert results == []
