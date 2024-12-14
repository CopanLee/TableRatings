FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && \
apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY . /app

RUN poetry install
