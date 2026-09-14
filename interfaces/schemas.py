from pydantic import BaseModel, Field, validator
from typing import List, Optional
from config import settings


class Analysis_Request(BaseModel):
  """Запрос на анализ одного текста"""
  text: str = Field(..., min_length=1, max_length=settings.max_text_length,
                      description='Текст для анализа')

  @validator('text')
  def validateText(cls, v):
    """Проверка, что текст не пустой"""
    if not v.strip():
      raise ValueError('Текст не может быть пустым')
    return v


class Batch_Request(BaseModel):
  """Запрос на анализ нескольких текстов"""
  texts: List[str] = Field(..., min_length=1, max_length=settings.max_batch_size,
                             description='Список текстов для анализа')

  @validator('texts')
  def validateTexts(cls, v):
    """Проверка, что все тексты не пустые"""
    for text in v:
      if not text.strip():
        raise ValueError('Текст в списке не может быть пустым')
    return v


#Ответы сервера.

class Text_Stats(BaseModel):
  """Статистика текста"""
  sentences: int = Field(..., description='Количество предложений')
  words: int = Field(..., description='Количество слов')
  syllables: int = Field(..., description='Количество слогов')
  avg_sentence_length: float = Field(..., description='Средняя длина предложения')
  avg_word_length: float = Field(..., description='Средняя длина слова')


class Flesch_Metrics(BaseModel):
  """Метрики Флеша"""
  index: float = Field(..., description='Индекс Флеша')
  level: str = Field(..., description='Уровень сложности')
  grade_level: Optional[float] = Field(None, description='Flesch-Kincaid Grade Level')


class Sentiment_Metrics(BaseModel):
  """Метрики тональности"""
  polarity: float = Field(..., ge=-1, le=1, description='Полярность (-1 до 1)')
  subjectivity: float = Field(..., ge=0, le=1, description='Субъективность (0 до 1)')
  sentiment: str = Field(..., description='Настроение: positive/neutral/negative')


class StatsSchema(BaseModel):
    sentence_count: int
    word_count: int
    syllable_count: int
    avg_sentence_length: float
    avg_word_syllables: float

class Analysis_Result(BaseModel):
    language: str
    flesch_index: float
    flesch_kincaid: float
    interpretation: str
    polarity: str
    subjectivity: float
    lexical_diversity: float
    rare_word_density: float
    stats: StatsSchema

class Analysis_Response(BaseModel):
    status: str
    result: Analysis_Result
    cached: bool
    processing_time: float

class Batch_Response(BaseModel):
    status: str
    results: list[Analysis_Result]
    cached: list[bool]
    total_time: float