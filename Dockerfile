FROM python:3.13-slim AS builder

ARG EXPORT_FLAG="--with dev"

RUN pip install --upgrade pip poetry poetry-plugin-export

COPY pyproject.toml poetry.toml poetry.lock ./

RUN poetry export -f requirements.txt $EXPORT_FLAG --without-hashes --output /tmp/requirements.txt


FROM python:3.13-slim

RUN apt-get update && \
  apt upgrade -y

WORKDIR /app

RUN groupadd -g 10000 app && \
  useradd -g app -d /app -u 10000 app && \
  chown app:app /app && \
  apt-get update && \
  apt-get install nano && \
  apt install -y gcc libpq-dev git gettext make postgresql && \
  pip install --upgrade pip

COPY --from=builder /tmp/requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py compilemessages && \
  python manage.py spectacular --file assets/schema.yml && \
  python manage.py collectstatic --noinput && \
  rm -fr /app/assets/*

USER app
