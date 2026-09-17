from pydantic_settings import BaseSettings #Проверять типы int, str..import
class Settings(BaseSettings): #Settings - класс, носит то, что носит BaseSettings
  """
  Настройки приложения.
  """
  app_name: str = "Text-Analysis"
  debug: bool = False #Режим отладки, показывающий ошибки.
  redis_url: str = "redis://localhost:6379/0" #Адрес редис для хранения памяти.
  cache_ttl_seconds: int = 3600 #Кеш ханится час.
  max_text_length: int = 10000
  batch_size_limit: int = 100
  log_level: str = "INFO" #В логе будет отображаться только основная информация.
  class Config: #Говорит, откуда брать настройки.
    env_file = ".env"
    env_file_encoding = "utf-8" #Кодировка файла.

settings = Settings() #Создала конкретный объект по шаблону, т.е. классу.

