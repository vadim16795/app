# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
ENV DBNAME='prod'
ENV USER='prod_app'
ENV PASSWORD='Oper@t10n!'
ENV HOST='34.79.66.203'
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
