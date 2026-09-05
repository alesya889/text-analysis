import redis, json, hashlib, logging
from typing import Optional, Any
from interfaces.schemas import Analysis_Result

logger = logging.getLogger(__name__)


class Cache_Service:
  """Сервис для работы с Redis кэшем."""
  def __init__(
    self,
    redisHost: str = 'localhost',
    redisPort: int = 6379,
    redisDb: int = 0,
    ttl: int = 6767
  ):
    """Инициализирует подключение к Redis."""
    self.ttl = ttl
    try:
      self.redis = redis.Redis(
        host=redisHost,
        port=redisPort,
        db=redisDb,
        decode_responses=True,
        socket_connect_timeout=2
      )
      self.redis.ping()
      logger.info(f'Подключение к Redis: {redisHost}:{redisPort}')
    except Exception as e:
      logger.error(f'Ошибка подключения к Redis: {e}')
      self.redis = None

  def _getKey(self, text: str) -> str:
    """Генерирует ключ для текста."""
    text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()
    return f'analysis:{text_hash}'

  def get_cached_result(self, text: str) -> Optional[Analysis_Result]:
    """Получает результат из кэша."""
    if not self.redis:
      return None

    try:
      key = self._getKey(text)
      cached = self.redis.get(key)

      if cached:
          data = json.loads(cached)
          logger.info(f'Найдено в кэше: {key[:20]}...')
          return Analysis_Result(**data)
      return None

    except Exception as e:
      logger.error(f'Ошибка чтения из кэша: {e}')
      return None

  def set_cached_result(self, text: str, result: Analysis_Result) -> bool:
    """Сохраняет результат в кэш."""
    if not self.redis:
      return False

    try:
      key = self._getKey(text)
      value = json.dumps(result.dict(), ensure_ascii=False, default=str)
      self.redis.setex(key, self.ttl, value)

      logger.info(f"✅ Сохранено в кэш: {key[:20]}... (TTL: {self.ttl}с)")
      return True

    except Exception as e:
      logger.error(f'Ошибка сохранения в кэш: {e}')
      return False

  def clear_cache(self, text: Optional[str] = None) -> bool:
    """Очищает кэш."""
    if not self.redis:
      return False

    try:
      if text:
        key = self._getKey(text)
        self.redis.delete(key)
        logger.info(f'Удален из кэша: {key[:20]}...')
      else:
        self.redis.flushdb()
        logger.info('Весь кэш очищен')
      return True

    except Exception as e:
      logger.error(f'Ошибка очистки кэша: {e}')
      return False

  def get_stats(self) -> dict:
    """Возвращает статистику кэша."""
    if not self.redis:
        return {"status": "not_connected"}
    try:
        keys = self.redis.keys("analysis:*")
        return {
            "status": "connected",
            "total_keys": len(keys),
            "ttl": self.ttl
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}