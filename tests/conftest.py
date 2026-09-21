import pytest


@pytest.fixture
def emptyString():
  # Фикстура: пустая строка.
  return ''


@pytest.fixture
def runner():
  # Тестовый клиент Click.
  return CliRunner()