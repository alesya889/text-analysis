import pytest
from infrastructure.syllable_counters import (
  countSyllablesEn,
  countSyllablesRu,
  countSyllablesGe,
  countSyllablesFr,
  getSyllableCounter
)
from domain.types import Languages_Used

"""Tests for counting syllables in different languages"""

class TestCountSyllablesEn:
  """Тесты для английского языка"""
  def test_simple_words(self):
    """Тест: простые слова"""
    assert countSyllablesEn('hello') == 2
    assert countSyllablesEn('world') == 1
    assert countSyllablesEn('mice') == 1
    assert countSyllablesEn('sun') == 1

  def test_complex_words(self):
    """Тест: сложные слова"""
    assert countSyllablesEn("banana") == 3
    assert countSyllablesEn("elephant") == 3
    assert countSyllablesEn("beautiful") == 3
    assert countSyllablesEn("unbelievable") == 5

  def test_upper_case(self):
    """Тест: слово в верхнем регистре"""
    assert countSyllablesEn("HELLO") == 2
    assert countSyllablesEn("WORLD") == 1

  def test_silent_e(self):
    """Тест: слова с немой 'e'"""
    assert countSyllablesEn("make") == 1
    assert countSyllablesEn("like") == 1
    assert countSyllablesEn("time") == 1

  def test_diphthongs(self):
    """Тест: слова с дифтонгами"""
    assert countSyllablesEn("house") == 1
    assert countSyllablesEn("boy") == 1
    assert countSyllablesEn("face") == 1


class TestCountSyllablesRu:
  """Тесты для русского языка"""

  def test_simple_words(self):
    """Тест: простые слова"""
    assert countSyllablesRu("привет") == 2
    assert countSyllablesRu("мама") == 2
    assert countSyllablesRu("мир") == 1
    assert countSyllablesRu("кот") == 1

  def test_complex_words(self):
    """Тест: сложные слова"""
    assert countSyllablesRu("здравствуйте") == 3
    assert countSyllablesRu("достопримечательность") == 7
    assert countSyllablesRu("этимология") == 6

  def test_with_yo(self):
    """Тест: слова с буквой ё"""
    assert countSyllablesRu("ёлка") == 2
    assert countSyllablesRu("подъём") == 2

  def test_uppercase(self):
    """Тест: слово в верхнем регистре"""
    assert countSyllablesRu("ПРИВЕТ") == 2
    assert countSyllablesRu("МИР") == 1


class TestCountSyllablesGe:
  """Тесты для немецкого языка"""

  def test_simple_words(self):
    """Тест: простые слова"""
    assert countSyllablesGe("hallo") == 2
    assert countSyllablesGe("welt") == 1
    assert countSyllablesGe("auto") == 2


class TestCountSyllablesFr:
  """Тесты для французского языка"""

  def test_simple_words(self):
    """Тест: простые слова"""
    assert countSyllablesFr("bonjour") == 2
    assert countSyllablesFr("monde") == 1
    assert countSyllablesFr("maison") == 2


class TestGetSyllableCounter:
  """Тесты для фабричной функции"""

  def test_get_english_counter(self):
    """Тест: получение счётчика для английского"""
    counter = getSyllableCounter(Languages_Used.ENGLISH)
    assert counter is not None
    assert counter("hello") == 2

  def test_get_russian_counter(self):
    """Тест: получение счётчика для русского"""
    counter = getSyllableCounter(Languages_Used.RUSSIAN)
    assert counter is not None
    assert counter("привет") == 2

  def test_get_german_counter(self):
    """Тест: получение счётчика для немецкого"""
    counter = getSyllableCounter(Languages_Used.GERMAN)
    assert counter is not None
    assert counter("hallo") == 2

  def test_get_french_counter(self):
    """Тест: получение счётчика для французского"""
    counter = getSyllableCounter(Languages_Used.FRANCE)
    assert counter is not None
    assert counter("bonjour") == 2

def test_empty_string(emptyString):
  """Тест: пустая строка"""
  assert countSyllablesEn(emptyString) == 0
  assert countSyllablesRu(emptyString) == 0
  assert countSyllablesGe(emptyString) == 1
  assert countSyllablesFr(emptyString) == 1