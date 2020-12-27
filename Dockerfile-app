FROM python:3

WORKDIR /app

COPY ./docker/app.ini ./

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./expense_logger ./expense_logger
COPY ./static ./static
COPY ./.env ./credentials.json ./

CMD [ "uwsgi", "--ini", "app.ini" ]