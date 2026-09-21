import pytest
from domain.types import TextStats
from infrastructure.flesch_calculators import fleschIndex, fleschKincaid
from domain.types import Languages_Used


def test_fleschIndex_english():
  # Проверяет индекс Флеша для английского текста.
  stats = TextStats(
    sentence_count=2,
    word_count=10,
    syllable_count=15,
    avg_sentence_length=5.0,
    avg_word_syllables=1.5,
  )
  result = fleschIndex(stats, Languages_Used.ENGLISH)
  expected = 206.835 - 1.015 * 5.0 - 84.6 * 1.5
  assert abs(result - expected) < 0.01


def test_fleschIndex_zero_values():
  # Проверяет индекс Флеша при нулевых значениях.
  stats = TextStats(
    sentence_count=0,
    word_count=0,
    syllable_count=0,
    avg_sentence_length=0.0,
    avg_word_syllables=0.0,
  )
  result = fleschIndex(stats, Languages_Used.ENGLISH)
  assert abs(result - 206.835) < 0.01


def test_fleschIndex_very_long():
  # Проверяет индекс Флеша для очень длинного текста.
  stats = TextStats(
    sentence_count=1,
    word_count=100,
    syllable_count=300,
    avg_sentence_length=100.0,
    avg_word_syllables=3.0,
  )
  result = fleschIndex(stats, Languages_Used.ENGLISH)
  assert result < 0


def test_fleschIndex_russian():
  # Проверяет индекс Флеша для русского текста.
  stats = TextStats(
    sentence_count=2,
    word_count=10,
    syllable_count=15,
    avg_sentence_length=5.0,
    avg_word_syllables=1.5,
  )
  result = fleschIndex(stats, Languages_Used.RUSSIAN)
  expected = 206.835 - 1.3 * 5.0 - 60.1 * 1.5
  assert abs(result - expected) < 0.01


def test_fleschIndex_german():
  # Проверяет индекс Флеша для немецкого текста.
  stats = TextStats(
    sentence_count=2,
    word_count=10,
    syllable_count=15,
    avg_sentence_length=5.0,
    avg_word_syllables=1.5
  )
  result = fleschIndex(stats, Languages_Used.GERMAN)
  expected = 206.835 - 1.015 * 5.0 - 84.6 * 1.5
  assert abs(result - expected) < 0.01


def test_fleschIndex_french():
  # Проверяет индекс Флеша для французского текста.
  stats = TextStats(
    sentence_count=2,
    word_count=10,
    syllable_count=15,
    avg_sentence_length=5.0,
    avg_word_syllables=1.5
  )
  result = fleschIndex(stats, Languages_Used.FRANCE)
  expected = 206.835 - 1.015 * 5.0 - 84.6 * 1.5
  assert abs(result - expected) < 0.01


def test_fleschKincaid_english():
  # Проверяет индекс Флеша-Кинкейда для английского текста.
  stats = TextStats(
    sentence_count=2,
    word_count=10,
    syllable_count=15,
    avg_sentence_length=5.0,
    avg_word_syllables=1.5
  )
  result = fleschKincaid(stats, Languages_Used.ENGLISH)
  expected = 0.39 * 5.0 + 11.8 * 1.5 - 15.59
  assert abs(result - expected) < 0.01


def test_fleschKincaid_german():
  # Проверяет индекс Флеша-Кинкейда для немецкого текста.
  stats = TextStats(
    sentence_count=2,
    word_count=10,
    syllable_count=15,
    avg_sentence_length=5.0,
    avg_word_syllables=1.5
  )
  result = fleschKincaid(stats, Languages_Used.GERMAN)
  expected = 0.39 * 5.0 + 11.8 * 1.5 - 15.59
  assert abs(result - expected) < 0.01


def test_fleschKincaid_frehch():
  # Проверяет индекс Флеша-Кинкейда для французского текста.
  stats = TextStats(
    sentence_count=2,
    word_count=10,
    syllable_count=15,
    avg_sentence_length=5.0,
    avg_word_syllables=1.5
  )
  result = fleschKincaid(stats, Languages_Used.FRANCE)
  expected = 0.39 * 5.0 + 11.8 * 1.5 - 15.59
  assert abs(result - expected) < 0.01


def test_fleschKincaid_russian():
  # Проверяет индекс Флеша-Кинкейда для русского текста.
  stats = TextStats(
    sentence_count=2,
    word_count=10,
    syllable_count=15,
    avg_sentence_length=5.0,
    avg_word_syllables=1.5)
  result = fleschKincaid(stats, Languages_Used.RUSSIAN)
  expected = 206.863 - (1.52 * 5.0) - (65.14 * 1.5)
  assert abs(result - expected) < 0.01


def test_fleschIndex_unsupported_language():
  # Проверяет ошибку при неподдерживаемом языке для индекса Флеша.
  stats = TextStats(
    sentence_count=2,
    word_count=10,
    syllable_count=15,
    avg_sentence_length=5.0,
    avg_word_syllables=1.5,
  )
  with pytest.raises(ValueError, match='Unsupported language'):
    fleschIndex(stats, 'spanish')


def test_fleschKincaid_unsupported_language():
  # Проверяет ошибку при неподдерживаемом языке для индекса Флеша-Кинкейда.
  stats = TextStats(
    sentence_count=2,
    word_count=10,
    syllable_count=15,
    avg_sentence_length=5.0,
    avg_word_syllables=1.5,
  )
  with pytest.raises(ValueError, match='Unsupported language'):
    fleschKincaid(stats, 'spanish')