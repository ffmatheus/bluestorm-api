FROM python:3.9-slim-buster

WORKDIR /code

# TODO: Multstage build, so the container does not runs with a compiler
RUN apt-get update && apt-get install curl build-essential unixodbc-dev wait-for-it -y

COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get remove build-essential -y

COPY ./api /code/

EXPOSE 8000