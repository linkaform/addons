####################################
# Image for develop                #
# MAINTAINER Linkaform
####################################

#FROM python:3.10.14-bullseye as develop
FROM python:3.12.12-slim-trixie AS develop

LABEL maintainer="Linkaform"

RUN apt-get update && \
    apt-get -y install \
    curl \
    gcc \
    gpg \
    git \
    libpq-dev \
    libffi-dev \
    poppler-utils \
    python3-psycopg2 \
    vim

#mongo 6.0 tools
RUN curl -fsSL https://pgp.mongodb.com/server-6.0.asc | gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
# trusted=yes: la clave de firma de MongoDB usa una firma SHA1 que Debian trixie rechaza (sqv) desde 2026-02-01
RUN echo "deb [ trusted=yes signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] http://repo.mongodb.org/apt/debian bullseye/mongodb-org/6.0 main" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list

RUN apt-get update && \
    apt-get -y install \
    mongodb-org-shell \
    mongodb-org-tools

COPY ./requires.txt /tmp/


RUN pip install --upgrade pip
# cx-Oracle 8.3.0 importa pkg_resources en setup.py; setuptools>=81 ya no lo trae
RUN pip install "setuptools<81" wheel && \
    pip install --no-build-isolation cx-Oracle==8.3.0
RUN pip install -r /tmp/requires.txt
RUN pip install --no-deps pdf2pptx==1.0.5

WORKDIR /usr/local/bin
#RUN git clone https://github.com/linkaform/backblaze_utils.git


ADD https://f001.backblazeb2.com/file/lkf-resources/linkaform_api-3.0.tar.gz ./linkaform_api-3.0.tar.gz
RUN pip install linkaform_api-3.0.tar.gz
ADD https://f001.backblazeb2.com/file/lkf-resources/backblaze_utils-0.1.tar.gz ./backblaze_utils-0.1.tar.gz
RUN pip install backblaze_utils-0.1.tar.gz
# RUN echo testsssssss
#RUN git clone https://github.com/linkaform/backblaze_utils.git
#WORKDIR /usr/local/bin/backblaze_utils



####################################
# Image for prodcution             #
####################################
FROM develop AS prod

LABEL maintainer="Linkaform"


COPY /requires.txt /tmp/

RUN pip install -r /tmp/requires.txt
