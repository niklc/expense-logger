FROM nginx:latest

ARG EMAIL
ARG DOMAIN

RUN mkdir -p /etc/letsencrypt/live/${DOMAIN}
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/letsencrypt/live/${DOMAIN}/privkey.pem \
  -out /etc/letsencrypt/live/${DOMAIN}/fullchain.pem \
  -subj "/C=LV/ST=Riga/L=Riga/O=Expense Logger/CN=${DOMAIN}/emailAddress=${EMAIL}}" \
  -addext "subjectAltName = DNS:${DOMAIN}"

RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048

RUN rm /etc/nginx/conf.d/default.conf
COPY ./docker/nginx-compose.conf /etc/nginx/templates/default.conf.template

COPY ./docker/options-ssl-nginx.conf /etc/nginx/snippets/