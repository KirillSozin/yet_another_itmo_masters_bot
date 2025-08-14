FROM python:3.14-rc-slim

# 2. Устанавливаем рабочую директорию
WORKDIR /app

# 3. Установка переменных окружения для Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Копирование файла с зависимостями и их установка
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копирование всего кода проекта в рабочую директорию
# Это включает папки app, scripts и data (для структуры)
COPY . .

# 6. Команда для запуска бота
# Используем флаг -m для корректного разрешения импортов
CMD ["python", "-m", "app.bot"]
