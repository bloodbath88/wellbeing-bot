# Dockerfile — запускает бота в контейнере
FROM python:3.12-slim

# Устанавливаем рабочую папку
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Инициализация базы данных
RUN python init_db.py

# Запускаем бота
CMD ["python", "main.py"]
