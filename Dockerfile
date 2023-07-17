FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update &&  \
    apt-get install -y --no-install-recommends software-properties-common build-essential libpq-dev && \
    pip3 install --upgrade pip && \
    pip3 install --upgrade setuptools && \
    pip3 install --upgrade wheel && \
    pip3 install poetry==1.5.1 --ignore-installed && \
    poetry config virtualenvs.create false && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

FROM base AS app

WORKDIR /home/app/

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-interaction --no-root

COPY ./delvify ./delvify
RUN poetry install --no-interaction --only-root

COPY ./migrations ./migrations
COPY ./alembic.ini ./alembic.ini

FROM app AS test

RUN poetry install --no-interaction --no-root --only test

COPY ./tests ./tests

CMD ["pytest"]
