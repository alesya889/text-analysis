from typing import Protocol
from domain.types import Languages_Used, Polarity

class SyllableCounter(Protocol):
  """
  Протокол для подсчета слогов в слове. Для роли 2,
  исп. в compute_stats, calculate_flesh_index.
  """
  def __call__(self, word: str) -> int:
    ...

class SentimentAnalyzer(Protocol):
  """
  Протокол для анализа тональности в тексте. Для роли 2,
  исп. в analyze_text.
  """
  def __call__(self, text: str) -> tuple[Polarity, float]:
    ...

class LanguageDetector(Protocol):
  """
  Протокол для определения языка текста. Для роли 2,
  исп. в analyze_text.
  """
  def __call__(self, text: str) -> Languages_Used:
    ...

class TextValidator(Protocol):
  """
  Протокол для валидации текста. Для роли 2,
  исп. в analyze_text, API.
  """
  def __call__(self, text: str) -> bool:
    ...

class StatsBuilder(Protocol):
  """
  Протокол для построения статистики текста. Для роли 2,
  исп. в analyze_text.
  """
  def __call__(self, text: str, syllable_counter: SyllableCounter) -> "TextStats":
    ...

class Cache(Protocol):
  """
  Протокол для кэширования результатов. Для роли 3,
  исп. В API.
  """
  def get(self, key: str) -> dict | None:
    ...
  def set(self, key: str, value: dict, ttl: int = 3600) -> None:
    ...
