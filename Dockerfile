FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update -qq && \
    apt-get install -y \
        mariadb-server mariadb-client \
        libmariadb-dev-compat libmariadb-dev libssl-dev curl

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

RUN mkdir /app
WORKDIR /app

# copy project files
COPY pyproject.toml poetry.lock /app/
COPY . /app/

# tell poetry to use system Python and install everything
RUN poetry config virtualenvs.create false --local && \
    poetry install --no-root --with test --no-interaction
