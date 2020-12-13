FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get -y install gcc
COPY ./requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /proj
COPY . /proj