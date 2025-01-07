# Same as in .tool-versions
FROM python:3.12.7-slim

# Standard Python config
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Project location
ENV PYTHONPATH="/app"
WORKDIR /app

# Project install (Poetry is faster than PIP despite having to install it first)
RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.4
ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Port for Chainlit UI
EXPOSE 8000

# Source code and CMD to be added in docker-compose.yml
