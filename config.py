class Settings():
  """Настройки приложения"""

  def __init__(self):
    self.redis_url = 'redis://localhost:6379/0'
    self.redis_ttl = 3600  #Время жизни кэша (1 час).
    self.api_host = '0.0.0.0'
    self.api_port = 8000
    self.max_text_length = 10000  #Максимальная длина текста в символах.
    self.max_batch_size = 100  #Максимальное количество текстов в пакете.
    self.cors_origins = ['*']  #Разрешить запросы с любых сайтов.
    self.log_level = 'INFO'
    self.log_format = 'console'  #Читаемый текст. можно поменять на "json".


settings = Settings()