from domain.types import Languages_Used
from domain.interfaces import (
  SyllableCounter,
  LanguageDetector,
  SentimentAnalyzer,
  TextValidator,
)


def getSyllableCounter(lang: Languages_Used) -> SyllableCounter:
  # Возвращает функцию подсчёта слогов для указанного языка.
  from infrastructure.syllable_counters import count_syllables_en
  return count_syllables_en


def getLanguageDetector() -> LanguageDetector:
  # Возвращает функцию определения языка.
  from infrastructure.language_detector import detect_language
  return detect_language


def getSentimentAnalyzer() -> SentimentAnalyzer:
  # Возвращает функцию анализа тональности.
  from infrastructure.sentiment import analyze_sentiment
  return analyze_sentiment


def getTextValidator() -> TextValidator:
  # Возвращает функцию валидации текста.
  from infrastructure.validator import validate_text
  return validate_text
