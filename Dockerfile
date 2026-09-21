FROM python:3.11-slim

# Создание папки app внутри контейнера и делает ее рабочей.
WORKDIR /app
# Установка компилятора gcc для сборки библиотек.
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Копирование всех файлов с комьютера  контейнер.
COPY . .
# Создаёт пользователя и даёт ему права на app.
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
# Запускает то, что внтури.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]