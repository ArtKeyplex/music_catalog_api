FROM python:3.11-slim-buster

WORKDIR /app
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "music_catalog.wsgi:application", "--bind", "0:8000" ]