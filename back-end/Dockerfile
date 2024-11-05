# syntax=docker/dockerfile:1

FROM --platform=linux/amd64 python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y gnupg wget chromium unzip

RUN DRIVER_VERSION=$(wget -O - https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE) \
 && wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/${DRIVER_VERSION}/linux64/chromedriver-linux64.zip
RUN unzip /tmp/chromedriver.zip -d /usr/local/bin/

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

EXPOSE 5000
COPY . .

CMD [ "flask", "run" ]
