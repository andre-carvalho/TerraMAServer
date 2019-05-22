# To build image for this dockerfile use this command:
#   docker build -t softwarevale/vita3server:0.1 --no-cache .
#
# To run without compose but with shell terminal use this command:
#   docker run -p 5000:5000 -v $PWD/api/storage_module/config:/server/api/storage_module/config -it softwarevale/vita3server:0.1 sh
#
# To run without compose and without shell terminal use this command:
#   docker run -p 5000:5000 -v $PWD/api/storage_module/config:/server/api/storage_module/config softwarevale/vita3server:0.1
#
#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM python:3.5-alpine

LABEL "br.inpe.dpi"="INPE/DPI-TerraMA" \
br.inpe.dpi.terrama="microservice" \
version="0.1" \
author="Andre Carvalho" \
author.email="andre.carvalho@inpe.br" \
description="This microservice receive an image \
files through upload from an Ionic app and provide \
access of those images over a REST API."

ENV PYTHONUNBUFFERED 1
#-------------Application Specific Stuff ----------------------------------------------------

ENV LIBRARY_PATH=/lib:/usr/lib

ENV INSTALL_PATH /server

COPY . $INSTALL_PATH/

RUN apk update \
  && apk add \
  postgresql \
  libpq \
  jpeg

RUN apk update \
  && apk add --no-cache \
    build-base \
    postgresql-dev \
    python-dev \
    py-pip \
    jpeg-dev \
    zlib-dev \
  && pip install --no-cache-dir -r $INSTALL_PATH/requirements.txt \
  && apk del build-base postgresql-dev python-dev py-pip jpeg-dev zlib-dev \
  && rm -rf /var/cache/apk/*

ENV APP_EXEC=$INSTALL_PATH/api/

EXPOSE 5000

VOLUME ["/server/api/storage_module/config", "/server/api/uploadImages"]

WORKDIR $APP_EXEC

CMD ["python", "server.py"]
