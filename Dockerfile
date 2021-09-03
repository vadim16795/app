# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
MAINTAINER vadim_arphipov@epam.com

ENV DB_NAME=prod
ENV DB_USER=postgres
ENV DB_PASSWORD=Oper@t10n
ENV DB_HOST=34.79.218.200

WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
CMD ["python3", "-m" , "flask", "run", "--port=5000","--host=0.0.0.0"]
