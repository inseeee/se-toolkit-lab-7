FROM python:3.12-slim

WORKDIR /app

# Копируем requirements (создадим его)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

CMD ["python", "bot.py"]
