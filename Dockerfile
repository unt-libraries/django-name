# vim: set ft=conf

FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update -qq && apt-get install -y python3 python-mysqldb mysql-client
RUN mkdir /app
WORKDIR /app
ADD requirements/ /app/requirements/
ADD requirements.txt /app/
RUN pip install -r requirements.txt
