FROM python:3.12-slim

WORKDIR /app

RUN apt update && apt install -y make

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY . .
