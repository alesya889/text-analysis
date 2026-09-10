import structlog #Библиотека для записи о том, что происходит в программе.
from contextlib import asynccontextmanager #Для FastAPI, что делать на старте, а что после.
from fastapi import FastAPI #Для создания приложения.
from fastapi.middleware.cors import CORSMiddleware #Разрешает запросы с других сайтов.
from config import settings

structlog.configure( #Настройка, как будут выглядеть соо в логах.
  processors=[
    structlog.processors.TimeStamper(fmt="iso"), #Время.
    structlog.processors.add_log_level, #Уровень лога: инфо, еррор, ворнинг.
    structlog.processors.JSONRenderer() #Выводит лог в формате JSON.
  ]
)
logger = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI): #Функция может работать параллельно с другими задачами.
  """
  Выполняется при запуске и остановке приложения.
  """
  logger.info("start application", app_name=settings.app_name)
  yield
  logger.info("end application")

app = FastAPI( #Объект, который обрабатывает HTTP-запросы
  title = settings.app_name, #Название в документации.**
  version = "1.0.0", #Версия API
  lifespan = lifespan,
  debug = settings.debug,
)

app.add_middleware( #Обработка запроса до попадания в основной код, обработка ответа до попадания к пользователю.
  CORSMiddleware, #Избежание блокировки API и веб сайта, так как у них разные localhost.
  allow_origins = ["*"], #Разрешать всем.
  allow_credentials = True,
  allow_methods = ["*"], #Все метододы
  allow_headers = ["*"], #Все заголовки: формат, язык ответа и пр.
)

@app.get("/") #Это декоратор (не меняя код, добавляет поведение). При GET-запросе на / вызвать функцию.
async def root():
  """
  Корневой адрес с информацией о сервисе.
  """
  return { #Из fastAPI в JSON.
    "service": settings.app_name,
    "version": "1.0.0",
    "docs": "/docs",
  }

@app.get("/health")
async def health():
  """
  Проверка работоспособности сайта.
  """
  return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
      "main:app",
      host="0.0.0.0", #Доступен с любого IP
      port=8000, #Для нахождения FastAPI
      reload=settings.debug #При изменении кода сервер перезапускаеся.
    )