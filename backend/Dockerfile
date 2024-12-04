# Используем базовый образ с Python 3.11
FROM python:3.11-slim

# Устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libffi-dev \
    libssl-dev \
    && apt-get clean

# Устанавливаем pip и обновляем его
RUN pip install --upgrade pip

# Устанавливаем зависимости проекта
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Копируем весь код проекта
COPY . /app/

# Открываем порт для приложения
EXPOSE 8000

# Запускаем сервер разработки Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
