FROM python:3.10.14-alpine3.19
RUN apk add build-base
RUN apk add libffi-dev
RUN mkdir /pythonApp
WORKDIR /pythonApp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src ./src
COPY .env .
WORKDIR /pythonApp/src