FROM python:3.11

WORKDIR /app

# Копируем файлы из корня проекта
COPY ../requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем остальной код
COPY . /app

# Запускаем FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]



