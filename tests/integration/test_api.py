"""
Интеграционные тесты для API
"""
import pytest
from fastapi.testclient import TestClient
from interfaces.api import app, cacheService


@pytest.fixture
def client():
  # Тестовый клиент FastAPI.
  with TestClient(app) as test_client:
    yield test_client
  # Очищаем кэш после тестов.
  try:
    cacheService.clear()
  except:
    pass


class TestHealthEndpoint:
  # Тесты эндпоинта /.

  def test_health_returns_ok(self, client):
    # GET / → 200 OK.
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


class TestAnalyzeEndpoint:
  # Тесты эндпоинта /analyze.

  def test_analyze_english_text(self, client):
    # POST /analyze с английским текстом.
    response = client.post('/analyze', json={
      'text': 'Hello world. This is a test.',
      'language': 'en'
    })
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert 'result' in data
    assert 'cached' in data
    assert data['cached'] is False

  def test_analyze_russian_text(self, client):
    # POST /analyze с русским текстом.
    response = client.post('/analyze', json={
      'text': 'Привет мир. Это тест.',
      'language': 'ru'
    })
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'

  def test_analyze_empty_text_returns_400(self, client):
    # POST /analyze с пустым текстом → 400.
    response = client.post('/analyze', json={
      'text': '',
      'language': 'en'
    })
    assert response.status_code == 400
    assert response.json()['status'] == 'error'

  def test_analyze_result_structure(self, client):
    # POST /analyze возвращает правильную структуру.
    response = client.post('/analyze', json={
      'text': 'Hello world. This is a test.',
      'language': 'en'
    })
    data = response.json()
    result = data['result']

    # Проверяем поля результата.
    assert 'language' in result
    assert 'flesch_index' in result
    assert 'flesch_kincaid' in result
    assert 'sentiment' in result
    assert 'stats' in result


class TestAnalyzeBatchEndpoint:
  # Тесты эндпоинта /analyze-batch.

  def test_analyze_batch_two_texts(self, client):
    # POST /analyze-batch с двумя текстами.
    response = client.post('/analyze-batch', json={
      'texts': [
        'Hello world.',
        'This is another test.'
      ]
    })
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == 'success'
    assert len(data['results']) == 2
    assert len(data['cached']) == 2

  def test_analyze_batch_empty_list(self, client):
    # POST /analyze-batch с пустым массивом.
    response = client.post('/analyze-batch', json={
      'texts': []
    })
    # Должно вернуть 400 или пустой результат.
    assert response.status_code in [200, 400, 422]

  def test_analyze_batch_result_structure(self, client):
    # POST /analyze-batch возвращает правильную структуру.
    response = client.post('/analyze-batch', json={
      'texts': ['Hello world.']
    })
    data = response.json()

    assert 'status' in data
    assert 'results' in data
    assert 'cached' in data
    assert 'total_time' in data


class TestCaching:
  # Тесты кэширования.


  def test_different_texts_not_cached(self, client):
    # Разные тексты не используют кэш друг друга.
    response1 = client.post('/analyze', json={
      'text': 'First unique text for cache test',
      'language': 'en'
    })
    response2 = client.post('/analyze', json={
      'text': 'Second unique text for cache test',
      'language': 'en'
    })

    assert response1.json()['cached'] is False
    assert response2.json()['cached'] is False


class TestErrorHandling:
  # Тесты обработки ошибок.

  def test_empty_text_returns_400(self, client):
    # Пустой текст → 400.
    response = client.post('/analyze', json={
      'text': '',
      'language': 'en'
    })
    assert response.status_code == 400

  def test_missing_text_field(self, client):
    # Отсутствует поле text → 400.
    response = client.post('/analyze', json={
      'language': 'en'
    })
    assert response.status_code == 400

  def test_unsupported_language(self, client):
    # Неподдерживаемый язык.
    response = client.post('/analyze', json={
      'text': 'Bonjour',
      'language': 'fr'  # Французский поддерживается.
    })
    # Должно работать или вернуть 400.
    assert response.status_code in [200, 400]

  def test_request_too_large(self, client):
    # Слишком большой запрос → 413.
    # Создаём текст больше 1 MB.
    large_text = 'a' * (1024 * 1024 + 100)
    response = client.post('/analyze', json={
      'text': large_text,
      'language': 'en'
    })
    assert response.status_code == 413