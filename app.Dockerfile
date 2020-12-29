FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./expense_logger ./expense_logger
COPY ./static ./static
COPY ./.env ./credentials.json ./

COPY ./docker/app.ini ./

CMD [ "uwsgi", "--ini", "app.ini" ]