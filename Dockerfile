# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
MAINTAINER vadim_arphipov@epam.com
ARG DB_NAME=mydb
ARG DB_USER=myuser
ARG DB_PASSWORD=mypassword
ARG DB_HOST=myhost
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
CMD ["python3", "-m" , "flask", "run", "--port=5000","--host=0.0.0.0"]
