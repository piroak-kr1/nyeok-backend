FROM python:3.12-slim

WORKDIR /project

# 1. Install irrelevant dependencies
RUN \
  --mount=type=cache,target=/var/cache/apt \
  apt update && \
  # Install psycopg2 dependencies
  apt install -y python3-dev libpq-dev gcc -y

# 2. Install dependencies (May break cache)
COPY requirements.txt ./
RUN pip install  --no-cache-dir -r requirements.txt

# 3. Local ./database_setup codes to Container /project/src
COPY ./database_setup /project/src

# Use .env.prod in env.py
ENV ENV=production

# alembic.ini is in /project/src
WORKDIR /project/src
CMD [ "alembic", "upgrade", "head" ]
