"""
НАСТРОЙКИ ПРОЕКТА
Читаются из переменных окружения (.env)
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  """Настройки приложения."""

  # Общие
  app_name: str = "Text Analyzer Service"
  debug: bool = False

  # API
  api_host: str = "0.0.0.0"
  api_port: int = 8000

  # Redis
  redis_url: str = "redis://localhost:6379/0"
  redis_ttl: int = 3600
  cache_ttl_seconds: int = 3600

  # Анализ
  max_text_length: int = 10000
  max_batch_size: int = 100
  batch_size_limit: int = 100

  # CORS
  cors_origins: list[str] = ["*"]

  # Логирование
  log_level: str = "INFO"
  log_format: str = "console"

  class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"


settings = Settings()