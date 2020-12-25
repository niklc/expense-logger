FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3-pip nginx

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt \
  -subj "" \
  -addext ""

RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

COPY ./nginx.conf /etc/nginx/sites-enabled/default
COPY ./self-signed.conf ./ssl-params.conf /etc/nginx/snippets/

WORKDIR /app

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./expense_logger ./expense_logger
COPY ./static ./static
COPY ./credentials.json ./

CMD service nginx start && \
    uwsgi -s /tmp/uwsgi.sock --chmod-socket=666 --manage-script-name --mount /=expense_logger:app