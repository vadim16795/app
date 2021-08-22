# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
MAINTAINER vadim_arphipov@epam.com
ENV HOST=$PROD_DB_HOST
ENV USER=$PROD_DB_USER
ENV PASSWORD=$PROD_DB_PASSWORD
ENV DBNAME=$PROD_DB_NAME
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]
