####################################
# Image for develop                #
####################################
FROM python:3.7-slim-bullseye as addons-base

MAINTAINER Linkaform

RUN apt-get update && \
    apt-get -y install \
    python3-psycopg2 \
    poppler-utils \
    libpq-dev \
    libffi-dev \
    gcc \
    gpg \
    curl \
    git \
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


####################################
# Image for develop                #
####################################
FROM linkaform/addons:base as develop


COPY ./docker/requires.txt /tmp/
COPY ./lkf_addons/bin/lkfaddons.py /usr/local/bin/lkfaddons
RUN chmod a+x /usr/local/bin/lkfaddons

RUN pip install --upgrade pip
RUN pip install -r /tmp/requires.txt

WORKDIR /tmp/
ADD https://f001.backblazeb2.com/file/lkf-resources/backblaze_utils-0.1.tar.gz ./backblaze_utils-0.1.tar.gz 
RUN pip install backblaze_utils-0.1.tar.gz

# RUN echo testsssssss
#RUN git clone https://github.com/linkaform/backblaze_utils.git
#WORKDIR /usr/local/bin/backblaze_utils
RUN rm /tmp/*.tar.gz

RUN mkdir -p /srv/scripts/addons/modules
RUN mkdir -p /srv/scripts/addons/config
WORKDIR /srv/scripts/addons/modules

####################################
# Image for prodcution             #
####################################
FROM develop as prod

MAINTAINER Linkaform

RUN echo teesttt
WORKDIR /tmp/
ADD  https://f001.backblazeb2.com/file/lkf-resources/linkaform_api-3.0.tar.gz ./linkaform_api-3.0.tar.gz
RUN pip install linkaform_api-3.0.tar.gz

#COPY ./docker/requires.txt /tmp/
# TODO COPIAR TODO ADDONS Y HACER IMAGEN.... AQUI O EN SCIRPTS?
COPY /lkf_addons /usr/local/lib/python3.7/site-packages/lkf_addons/
COPY ./config /srv/scripts/addons/config


#RUN pip install -r /tmp/requires.txt
