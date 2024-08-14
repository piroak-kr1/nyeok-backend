FROM python:3.12-slim

RUN pip install poetry==1.8.3

# 1. install dependencies
ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_IN_PROJECT=1 \
  POETRY_VIRTUALENVS_CREATE=1 \
  POETRY_CACHE_DIR=/tmp/poetry_cache

COPY pyproject.toml poetry.lock README.md /APP/

WORKDIR /APP

RUN poetry install && rm -rf $POETRY_CACHE_DIR

# 2. Copy codes: Local ./app to Container /APP
COPY ./app /APP

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app.py when the container launches
CMD ["poetry", "run", "fastapi", "dev", "--port", "8000", "--host", "0.0.0.0"]
