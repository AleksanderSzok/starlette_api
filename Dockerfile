FROM python:3.10.0-alpine

WORKDIR /src

COPY ./app /src/app

COPY ./requirements.txt /src/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
