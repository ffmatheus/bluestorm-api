FROM python:3.9-slim-buster

WORKDIR /code

# TODO: Multstage build, so the container does not runs with a compiler
RUN apt-get update && apt-get install curl build-essential unixodbc-dev wait-for-it -y

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

RUN pip install --upgrade pip

# Install app deps
COPY ./pyproject.toml ./pytest.ini /code/
RUN poetry install

# Removes compliler
RUN apt-get remove build-essential -y

COPY ./api /code/api/

CMD ["uvicorn", "api.main:app", "--host=0.0.0.0", "--port=8000"]

EXPOSE 8000