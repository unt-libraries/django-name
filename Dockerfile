FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH="/root/.local/bin:$PATH"

RUN apt-get update -qq && \
    apt-get install -y \
        python3-venv \
        mariadb-server mariadb-client \
        libmariadb-dev-compat libmariadb-dev libssl-dev curl

WORKDIR /app

# copy project files
COPY pyproject.toml poetry.lock /app/
COPY . /app/

# install dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install ".[test,dev,codestyle]"

