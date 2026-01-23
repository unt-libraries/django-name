FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update -qq && \
    apt-get install -y \
        mariadb-server mariadb-client \
        libmariadb-dev-compat libmariadb-dev libssl-dev

WORKDIR /app

# copy project files
COPY . /app/

# install dependencies
RUN pip install .'[dev,test,codestyle]'
