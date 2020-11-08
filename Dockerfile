FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y python3-pip

RUN pip3 install uwsgi==2.0.18 flask==1.1.2

COPY wsgi.py app/wsgi.py

EXPOSE 8080

# cd app
# uwsgi --socket :8080 --protocol=http -w wsgi