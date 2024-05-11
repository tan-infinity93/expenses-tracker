# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
COPY ./requirements.txt /tmp/requirements.txt
RUN apt-get update -y && apt-get install vim -y --fix-missing 
RUN apt-get install curl -y --fix-missing && apt-get install -y procps --fix-missing
RUN pip install -r /tmp/requirements.txt
COPY ./ /home/src/
WORKDIR /home/src/
ENV ENV=production
ENV PYTHONUNBUFFERED=True
CMD gunicorn -b 0.0.0.0:5000 --capture-output main:app -w 1 -t 10
