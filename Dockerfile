FROM python:3.12-slim

WORKDIR /backend

# 1. Install irrelevant dependencies
RUN pip install poetry==1.8.3

RUN \
  --mount=type=cache,target=/var/cache/apt \
  apt update && \
  # Install psycopg2 dependencies
  apt install -y python3-dev libpq-dev gcc -y

# 2. Install poetry's dependencies (Always cache break)
COPY pyproject.toml poetry.lock README.md ./

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

RUN --mount=type=cache,target=/root/.cache poetry config cache-dir /root/.cache && \
  poetry install && rm -rf $POETRY_CACHE_DIR

# 3. Local ./app codes to Container /backend/app
COPY ./app ./app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Move to /backend/app and run /backend/app/main.py
CMD ["poetry", "run", "bash", "-c", "cd app && fastapi dev --port 8000 --host 0.0.0.0"]
