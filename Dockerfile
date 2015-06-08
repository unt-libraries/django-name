# vim: set ft=conf

FROM python:2.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app
ENV TOXENV=py27-django{16,17,18}-{mysql,postgres},flake8,docs
RUN apt-get update -qq && apt-get install -y python-mysqldb mysql-client
RUN mkdir /app
WORKDIR /app
ADD requirements/ /app/requirements/
ADD requirements.txt /app/
RUN pip install -r requirements.txt
