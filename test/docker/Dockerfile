####################################
# Image for develop                #
####################################

FROM python:3.7-bullseye as develop

MAINTAINER Linkaform


#mongo 5.0 tools
RUN curl -fsSL https://pgp.mongodb.com/server-5.0.asc | gpg -o /usr/share/keyrings/mongodb-server-5.0.gpg --dearmor
RUN echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-5.0.gpg] http://repo.mongodb.org/apt/debian bullseye/mongodb-org/5.0 main" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list

RUN apt-get update && \
    apt-get -y install \
    python3-psycopg2 \
    poppler-utils \
    mongodb-org-shell \
    mongodb-org-tools

COPY ./requires.txt /tmp/


RUN pip install --upgrade pip
RUN pip install -r /tmp/requires.txt

WORKDIR /usr/local/bin
#RUN git clone https://github.com/linkaform/backblaze_utils.git


RUN echo te
RUN wget  --no-check-certificate https://f001.backblazeb2.com/file/lkf-resources/linkaform_api-3.0.tar.gz
RUN pip install linkaform_api-3.0.tar.gz
RUN wget --no-check-certificate  https://f001.backblazeb2.com/file/lkf-resources/backblaze_utils-0.1.tar.gz
RUN pip install backblaze_utils-0.1.tar.gz
# RUN echo testsssssss
#RUN git clone https://github.com/linkaform/backblaze_utils.git
#WORKDIR /usr/local/bin/backblaze_utils



####################################
# Image for prodcution             #
####################################
FROM develop as prod

MAINTAINER Linkaform


COPY /requires.txt /tmp/

RUN pip install -r /tmp/requires.txt
