FROM ubuntu:18.04
FROM python:3.8.3-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y

COPY ./requirements.txt /requirements.txt

# Install postgres client
#RUN apk add --update --no-cache postgresql-client

# Install individual dependencies
# so that we could avoid installing extra packages to the container
#RUN apk add --update --no-cache --virtual .tmp-build-deps \
#	gcc libc-dev linux-headers postgresql-dev

RUN apt install gdal-bin libgdal-dev -y
RUN apt install python3-gdal -y
RUN apt install binutils libproj-dev -y


RUN pip install -r /requirements.txt

# Remove dependencies
#RUN apk del .tmp-build-deps

RUN mkdir /ubiwhere_challenge
WORKDIR /ubiwhere_challenge
COPY ./ubiwhere_challenge /ubiwhere_challenge

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# [Security] Limit the scope of user who run the docker image
#RUN adduser -D user

#USER user