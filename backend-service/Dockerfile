FROM python:3.12-slim

WORKDIR /backend

# 1. Install irrelevant dependencies
RUN \
  --mount=type=cache,target=/var/cache/apt \
  apt update && \
  # Install psycopg2 dependencies
  apt install -y python3-dev libpq-dev gcc -y

# 2. Install dependencies (May break cache)
COPY requirements.txt ./
RUN pip install  --no-cache-dir -r requirements.txt

# 3. Local ./backend_service codes to Container /backend/app
COPY ./backend_service ./app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Move to /backend/app and run /backend/app/main.py
# TODO: Use JSON for CMD
CMD fastapi dev --root-path ${ROOT_PATH:-/} --port 8000 --host 0.0.0.0
