FROM python:3.9-slim-buster

WORKDIR /code

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./api /code/api/

EXPOSE 8000