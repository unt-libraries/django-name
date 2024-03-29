# vim: set ft=conf

FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app
ENV PYTHONDONTWRITEBYTECODE 1
RUN apt-get update -qq && \
    apt-get install -y mariadb-server mariadb-client libmariadb-dev-compat libmariadb-dev libssl-dev
RUN mkdir /app
WORKDIR /app
ADD requirements/ /app/requirements/
ADD requirements.txt /app/
RUN pip install -r requirements.txt
