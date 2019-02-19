# To build image for this dockerfile use this command:
#   docker build -t softwarevale/mobile-server:v3 -f env/Dockerfile .
#
# To run without compose but with shell terminal use this command:
#   docker run -p 8081:8000 --name tma-attempo-server --rm -v /data/mobile/attempo_files:/server/utils/uploadImages -it softwarevale/mobile-server:v3 sh
#
# To run without compose and without shell terminal use this command:
#   docker run -p 8081:8000 --name tma-attempo-server --rm -v /data/mobile/attempo_files:/server/utils/uploadImages -d softwarevale/mobile-server:v3
#
#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM python:3.6-alpine

LABEL "br.inpe.dpi"="INPE/DPI-TerraMA" \
br.inpe.dpi.terrama="microservice" \
version="0.3" \
author="Andre Carvalho" \
author.email="andre-carvalho@inpe.br" \
description="This microservice receive image \
files through upload from an Ionic app and provide \
access of those images over a REST API."

ENV PYTHONUNBUFFERED 1
#-------------Application Specific Stuff ----------------------------------------------------

RUN apk update \
  && apk add --no-cache --update \
    build-base \
    postgresql \
    postgresql-dev \
    libpq \
    python-dev \
    py-pip \
    jpeg-dev \
    zlib-dev \
    tzdata

ENV TZ=America/Sao_Paulo

ENV LIBRARY_PATH=/lib:/usr/lib

ENV INSTALL_PATH /server

COPY api $INSTALL_PATH/api
COPY utils $INSTALL_PATH/utils

# Install Python requirements
RUN pip install -r $INSTALL_PATH/utils/requirements.txt

EXPOSE 8000

VOLUME ["/server/api/uploadImages"]

WORKDIR $INSTALL_PATH/api

# new way using the gunicorn as a WSGI server
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "wsgi:app"]
