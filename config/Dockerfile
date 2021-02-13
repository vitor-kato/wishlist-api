# syntax = docker/dockerfile:1.0-experimental

FROM python:3.8.7-buster as base

ENV PYTHONWARNINGS ignore
ENV PYTHONUNBUFFERED 1

ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then pip install jupyterlab ; fi"

COPY requirements.txt .

RUN pip install -Ur requirements.txt --quiet
WORKDIR /webapps


FROM base as develop
ENTRYPOINT ["/webapps/docker-entrypoint.sh"]


FROM base as prod
COPY . .
ENTRYPOINT ["/webapps/docker-entrypoint.sh"]
