# To build image for this dockerfile use this command:
#   docker build -t attempo-server:v2 -f env/Dockerfile .
#
# To run without compose but with shell terminal use this command:
#   docker run -p 80:5000 --name tma-attempo-server --rm -v /tmp/docker_server:/server -it attempo-server:v1 sh
#
# To run without compose and without shell terminal use this command:
#   docker run -p 80:5000 --name tma-attempo-server --rm -v /tmp/docker_server:/server -d attempo-server:v1
#
#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM python:3.5-alpine

LABEL "br.inpe.dpi"="INPE/DPI-TerraMA" \
br.inpe.dpi.terrama="microservice" \
version="0.2" \
author="Andre Carvalho" \
author.email="andre-carvalho@inpe.br" \
description="This microservice receive image \
files through upload from an Ionic app and provide \
access of those images over a REST API."

ENV PYTHONUNBUFFERED 1
#-------------Application Specific Stuff ----------------------------------------------------

RUN apk update \
  && apk add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq \
    python-dev \
    py-pip \
    jpeg-dev \
    zlib-dev

ENV LIBRARY_PATH=/lib:/usr/lib

ENV INSTALL_PATH /server

COPY api $INSTALL_PATH/api
COPY utils $INSTALL_PATH/utils

# Install Python requirements
RUN pip install -r $INSTALL_PATH/utils/requirements.txt

# Set permission to exec
# RUN chmod +x ${INSTALL_PATH}/utils/prepare_db.sh

ENV APP_EXEC=$INSTALL_PATH/utils/

EXPOSE 5000

VOLUME ["/server/utils/uploadImages"]

WORKDIR $APP_EXEC

# Start service using a shell script. Try create postgis extension and table into target database.
# I thing that this way of starting service is wrong. Locked the service after some time.
#ENTRYPOINT ./prepare_db.sh

# The regular way is better, i think
CMD ["python", "/server/api/server.py"]
