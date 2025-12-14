####################################
# Image for develop                #
####################################
#FROM python:3.7-slim-bullseye as addons-base
FROM python:3.10.14-bullseye as addons-base


MAINTAINER Linkaform

RUN apt-get update && \
    apt-get -y install \
    curl \
    gcc \
    gpg \
    git \.
    libpq-dev \
    libffi-dev \
    poppler-utils \
    python3-psycopg2 \
    time \
    vim

#mongo 5.0 tools
RUN curl -fsSL https://pgp.mongodb.com/server-5.0.asc | gpg -o /usr/share/keyrings/mongodb-server-5.0.gpg --dearmor
RUN echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-5.0.gpg] http://repo.mongodb.org/apt/debian bullseye/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list

RUN apt-get update && \
    apt-get -y install \
    python3-psycopg2 \
    libpq-dev \
    poppler-utils \
    mongodb-org-shell \
    mongodb-org-tools

COPY ./secrets/lkf_jwt_key.pub /etc/ssl/certs/lkf_jwt_key.pub
COPY ./lkfpwd.py /usr/local/lib/python3.10


WORKDIR /srv/scripts/addons/modules

####################################
# Image for develop                #
####################################
FROM linkaform/addons:base as develop


COPY ./docker/requires.txt /tmp/
COPY ./lkf_addons/bin/lkfaddons.py /usr/local/bin/lkfaddons
RUN chmod a+x /usr/local/bin/lkfaddons

RUN pip install --upgrade pip
RUN pip install -r /tmp/requires.txt
RUN pip install twilio
RUN pip install git+https://github.com/Bastian-Kuhn/wallet.git
WORKDIR /tmp/
ADD https://f001.backblazeb2.com/file/lkf-resources/backblaze_utils-0.1.tar.gz ./backblaze_utils-0.1.tar.gz 
RUN pip install backblaze_utils-0.1.tar.gz

# RUN echo testsssssss
#RUN git clone https://github.com/linkaform/backblaze_utils.git
#WORKDIR /usr/local/bin/backblaze_utils
RUN rm /tmp/*.tar.gz

RUN adduser --home /srv/scripts/ --uid 1000 --disabled-password nonroot
RUN mkdir -p /srv/scripts/addons/modules
RUN mkdir -p /srv/scripts/addons/config
RUN chown -R 1000:1000 /srv/scripts
WORKDIR /srv/scripts/addons/modules

####
# Oracle Integration
###
WORKDIR /opt/oracle
ADD https://f001.backblazeb2.com/file/app-linkaform/public-client-126/71202/6650c41a967ad190e6a76dd3/66b5974cae333f423347115c.zip  66b5974cae333f423347115c.zip
RUN unzip 66b5974cae333f423347115c.zip
RUN cd /opt/oracle/instantclient_12_2/
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient:$LD_LIBRARY_PATH

RUN apt-get install libaio1
RUN echo /opt/oracle/instantclient_12_2 > /etc/ld.so.conf.d/oracle-instantclient.conf
RUN ldconfig

### END ORACLE ###

# USER nonroot

WORKDIR /srv/scripts/addons/modules

####################################
# Image for prodcution             #
####################################
FROM develop as prod


USER root
RUN echo teesttt
WORKDIR /tmp/
ADD  https://f001.backblazeb2.com/file/lkf-resources/linkaform_api-3.0.tar.gz ./linkaform_api-3.0.tar.gz
RUN pip install linkaform_api-3.0.tar.gz

#COPY ./docker/requires.txt /tmp/
# TODO COPIAR TODO ADDONS Y HACER IMAGEN.... AQUI O EN SCIRPTS?
COPY /lkf_addons /usr/local/lib/python3.10/site-packages/lkf_addons/
COPY ./config /srv/scripts/addons/config

RUN chown -R 33:33 /srv/scripts

USER www-data

#RUN pip install -r /tmp/requires.txt
WORKDIR /srv/scripts/addons/modules
