from fastapi.testclient import TestClient
import interfaces.api as api
from interfaces.api import app

#Фейковый кэш вместо Redis.

class FakeCacheService:
  def __init__(self):
    self.data = {}

  def getCachedResult(self, text):
    return self.data.get(text)

  def setCachedResult(self, text, result):
    self.data[text] = result

api.cacheService = FakeCacheService()
client = TestClient(app)

#/health

def testHealth():
  response = client.get('/health')

  assert response.status_code == 200

  data = response.json()

  assert data['status'] == 'ok'

#/analyze

def testAnalyzeText():
  response = client.post(
    '/analyze',
    json={
      'text': 'Hello, this is a simple test.'
    }
  )

  assert response.status_code == 200

  data = response.json()

  #Проверяем ответ верхнего уровня
  assert data['status'] == 'success'
  assert data['cached'] is False
  assert 'processing_time' in data

  #Проверяем result
  result = data['result']

  assert 'language' in result
  assert 'flesch_index' in result
  assert 'flesch_kincaid' in result
  assert 'interpretation' in result
  assert 'polarity' in result
  assert 'subjectivity' in result
  assert 'lexical_diversity' in result
  assert 'rare_word_density' in result
  assert 'stats' in result

  #Проверяем статистику
  stats = result['stats']

  assert 'sentence_count' in stats
  assert 'word_count' in stats
  assert 'syllable_count' in stats
  assert 'avg_sentence_length' in stats
  assert 'avg_word_syllables' in stats


def testAnalyzeEmptyText():
  response = client.post(
    '/analyze',
    json={
      'text': ''
    }
  )

  assert response.status_code == 422


def testAnalyzeWhitespaceText():
  response = client.post(
    '/analyze',
    json={
      'text': '     '
    }
  )

  assert response.status_code == 422


def testAnalyzeMissingText():
  response = client.post(
    '/analyze',
    json={}
  )

  assert response.status_code == 422

#Проверка кэша

def testAnalyzeCachedText():
  text = 'This is a cached text.'

  #Первый запрос
  response1 = client.post(
    '/analyze',
    json={
      'text': text
    }
  )

  assert response1.status_code == 200

  data1 = response1.json()

  assert data1['cached'] is False

  #Второй запрос
  response2 = client.post(
    '/analyze',
    json={
      'text': text
    }
  )

  assert response2.status_code == 200

  data2 = response2.json()

  assert data2['cached'] is True

#/analyze-batch


def testAnalyzeBatch():
  response = client.post(
    '/analyze-batch',
    json={
      'texts': [
        'Hello, this is the first text.',
        'Hello, this is the second text.'
      ]
    }
  )

  assert response.status_code == 200

  data = response.json()

  #Проверяем основной ответ
  assert data['status'] == 'success'
  assert 'results' in data
  assert 'cached' in data
  assert 'total_time' in data

  #Должно быть 2 результата
  assert len(data['results']) == 2

  #Для каждого текста должен быть свой cached
  assert len(data['cached']) == 2

  #Проверяем первый результат
  result = data['results'][0]

  assert 'language' in result
  assert 'flesch_index' in result
  assert 'flesch_kincaid' in result
  assert 'interpretation' in result
  assert 'polarity' in result
  assert 'subjectivity' in result
  assert 'lexical_diversity' in result
  assert 'rare_word_density' in result
  assert 'stats' in result


def testAnalyzeBatchEmptyList():
  response = client.post(
    '/analyze-batch',
    json={
      'texts': []
    }
  )

  assert response.status_code == 422


def testAnalyzeBatchWithEmptyText():
  response = client.post(
    '/analyze-batch',
    json={
      'texts': [
        'Hello world.',
        ''
      ]
    }
  )

  assert response.status_code == 422


def testAnalyzeBatchWithWhitespaceText():
  response = client.post(
    '/analyze-batch',
    json={
      'texts': [
        'Hello world.',
        '     '
      ]
    }
  )

  assert response.status_code == 422


def testAnalyzeBatchMissingTexts():
  response = client.post(
    '/analyze-batch',
    json={}
  )

  assert response.status_code == 422