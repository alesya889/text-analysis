import pytest
from click.testing import CliRunner


@pytest.fixture
def emptyString():
    # Фикстура: пустая строка.
    return ""


@pytest.fixture
def runner():
    # Тестовый клиент Click.
    return CliRunner()
