# Dockerfile — запускает бота в контейнере
FROM python:3.12-slim

# Устанавливаем рабочую папку
WORKDIR /app

# Копируем все файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Создаём базу данных при первом запуске
RUN python init_db.py

# Запускаем бота
CMD ["python", "main.py"]