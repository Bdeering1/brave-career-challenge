# syntax=docker/dockerfile:1

FROM python:3.12-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 5000
COPY . .

CMD [ "flask", "run" ]
