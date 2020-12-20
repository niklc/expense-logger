FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3-pip nginx

COPY ./ ./app
WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./nginx.conf /etc/nginx/sites-enabled/default

CMD service nginx start && \
    uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=expense_logger:app