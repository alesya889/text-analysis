"""
Типы данных проекта, которые другие роли будут использовать в дальнейшей работе.
"""
from dataclasses import dataclass #Классы напоминают словари, это для быстрого обращения.
from enum import Enum #Для фиксированных наборов значений, по типу языков.
from typing import Dict, Tuple

class Languages_Used(Enum):
  """
  Все поддерживаемые языки.
  """
  ENGLISH = 'en'
  RUSSIAN = 'ru'

class Polarity(Enum):
  Positive = 'positive'
  Negative = 'negative'
  Neutral = 'neutral'

class Difficulty_Level(Enum):
  Very_Easy = 'very_easy'
  Easy = 'easy'
  Hard = 'hard'
  Very_Hard = 'very_hard'

FleshCoefficients: Dict[Languages_Used, Tuple[float, float, float]] = {
  Languages_Used.ENGLISH: (206.835, 1.015, 84.6),
  Languages_Used.RUSSIAN: (206.835, 1.3, 60.1)
}

@dataclass(frozen=True)
class TextStats:
  sentence_count: int #Количество предложений.
  word_count: int #Количество слов.
  syllable_count: int #Количество слогов.
  avg_sentence_length: float #Средняя длина предложений.
  avg_word_syllables: float #Средняя длина слова.

@dataclass(frozen=True)
class AnalysisResult:
  """
  Результат анализа текста.
  """
  language: Languages_Used
  flesch_index: float
  flesch_kincaid: float
  interpretation: str #Восприятие.
  polarity: Polarity #Тональность.
  subjectivity: float #Субъективность
  lexical_diversity: float #Лексическое разнообразие.
  rare_word_density: float #Плотность редких слов.
  stats: TextStats #Статистика текста.

  def to_dict(self):
    """"
    Превратит объекты выше в словари,
    чтобы далее для роли 2 и 3 не вознакало проблем с API и прочее.
    """
    return {
      "language": self.language.value,
      "flesch_index": round(self.flesch_index, 2),
      "flesch_kincaid": round(self.flesch_kincaid, 2),
      "interpretation": self.interpretation,
      "polarity": self.polarity.value,
      "subjectivity": round(self.subjectivity, 2),
      "lexical_diversity": round(self.lexical_diversity, 2),
      "rare_word_density": round(self.rare_word_density, 2),
      "stats": {
          "sentence_count": self.stats.sentence_count,
          "word_count": self.stats.word_count,
          "syllable_count": self.stats.syllable_count,
          "avg_sentence_length": round(self.stats.avg_sentence_length, 2),
          "avg_word_syllables": round(self.stats.avg_word_syllables, 2),
      }
    }

  @classmethod
  def from_dict(cls, data: dict):
    """
    Из словаря в другой объект.
    """
    stats = TextStats(
      sentence_count=data["stats"]["sentence_count"],
      word_count=data["stats"]["word_count"],
      syllable_count=data["stats"]["syllable_count"],
      avg_sentence_length=data["stats"]["avg_sentence_length"],
      avg_word_syllables=data["stats"]["avg_word_syllables"],
    )
    return cls(
      language=Languages_Used(data["language"]),
      flesch_index=data["flesch_index"],
      flesch_kincaid=data["flesch_kincaid"],
      interpretation=data["interpretation"],
      polarity=Polarity(data["polarity"]),
      subjectivity=data["subjectivity"],
      lexical_diversity=data["lexical_diversity"],
      rare_word_density=data["rare_word_density"],
      stats=stats,
    )

