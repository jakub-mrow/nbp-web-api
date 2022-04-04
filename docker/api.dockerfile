FROM python:3.9.7-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE=1

COPY docker/requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /api
COPY . .

WORKDIR /api/app

EXPOSE 8000

LABEL maintainer jakub-mrow
LABEL Project=nbp-api