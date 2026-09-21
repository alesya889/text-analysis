"""
Интеграционные тесты для CLI
"""
import pytest
import json
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from interfaces.cli import cli


@pytest.fixture
def runner():
  """Тестовый клиент Click"""
  return CliRunner()


class TestAnalyzeCommand:
  """Тесты команды analyze"""

  def test_analyze_text_success(self, runner):
    """Тест: analyze --text"""
    with patch('interfaces.cli.httpx.post') as mock_post:
      # Настраиваем mock-ответ
      mock_response = MagicMock()
      mock_response.status_code = 200
      mock_response.json.return_value = {
        "status": "success",
        "result": {"language": "English", "flesch_index": 85.0}
      }
      mock_post.return_value = mock_response

      result = runner.invoke(cli, ['analyze', '--text', 'Hello world'])

      assert result.exit_code == 0
      assert 'success' in result.output

  def test_analyze_file_success(self, runner, tmp_path):
    """Тест: analyze --file"""
    # Создаём временный файл
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello world from file", encoding='utf-8')

    with patch('interfaces.cli.httpx.post') as mock_post:
      mock_response = MagicMock()
      mock_response.status_code = 200
      mock_response.json.return_value = {
        "status": "success",
        "result": {"language": "English"}
      }
      mock_post.return_value = mock_response

      result = runner.invoke(cli, ['analyze', '--file', str(file_path)])

      assert result.exit_code == 0

  def test_analyze_batch_file_success(self, runner, tmp_path):
    """Тест: analyze --batch-file"""
    # Создаём временный файл с несколькими текстами
    file_path = tmp_path / "batch.txt"
    file_path.write_text(
      "First text\nSecond text\nThird text",
      encoding='utf-8'
    )

    with patch('interfaces.cli.httpx.post') as mock_post:
      mock_response = MagicMock()
      mock_response.status_code = 200
      mock_response.json.return_value = {
        "status": "success",
        "results": [{"language": "English"}, {"language": "English"}]
      }
      mock_post.return_value = mock_response

      result = runner.invoke(cli, ['analyze', '--batch-file', str(file_path)])

      assert result.exit_code == 0


class TestAnalyzeErrors:
  """Тесты ошибок команды analyze"""

  def test_analyze_no_arguments(self, runner):
    """Тест: analyze без аргументов → ошибка"""
    result = runner.invoke(cli, ['analyze'])

    assert result.exit_code != 0
    assert 'Укажите --text, --file или --batch-file' in result.output

  def test_analyze_multiple_arguments(self, runner, tmp_path):
    """Тест: analyze с несколькими аргументами → ошибка"""
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello", encoding='utf-8')

    result = runner.invoke(cli, [
      'analyze',
      '--text', 'Hello',
      '--file', str(file_path)
    ])

    assert result.exit_code != 0
    assert 'Можно использовать только один' in result.output


class TestApiErrors:
  """Тесты обработки ошибок API"""

  def test_api_returns_400(self, runner):
    """Тест: API возвращает 400"""
    with patch('interfaces.cli.httpx.post') as mock_post:
      mock_response = MagicMock()
      mock_response.status_code = 400
      mock_response.text = '{"status": "error", "message": "Invalid text"}'
      mock_post.return_value = mock_response

      result = runner.invoke(cli, ['analyze', '--text', ''])

      assert 'Ошибка 400' in result.output

  def test_api_returns_500(self, runner):
    """Тест: API возвращает 500"""
    with patch('interfaces.cli.httpx.post') as mock_post:
      mock_response = MagicMock()
      mock_response.status_code = 500
      mock_response.text = 'Internal server error'
      mock_post.return_value = mock_response

      result = runner.invoke(cli, ['analyze', '--text', 'Hello'])

      assert 'Ошибка 500' in result.output


class TestCLIGroup:
  """Тесты главной группы CLI"""

  def test_cli_help(self, runner):
    """Тест: cli --help"""
    result = runner.invoke(cli, ['--help'])

    assert result.exit_code == 0
    assert 'analyze' in result.output

  def test_analyze_help(self, runner):
    """Тест: analyze --help"""
    result = runner.invoke(cli, ['analyze', '--help'])

    assert result.exit_code == 0
    assert '--text' in result.output
    assert '--file' in result.output
    assert '--batch-file' in result.output
