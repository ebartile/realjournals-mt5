FROM elestio/metatrader5:latest

LABEL maintainer="info@realjournals.com"

USER root

ENV HOME /home/kasm-user
WORKDIR $HOME
RUN chown -R root:root $HOME

ARG APP_ENV
ARG DEBIAN_FRONTEND=noninteractive
ARG HOST_GID

ENV TZ=UTC
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

### Install various tools
RUN apt update
RUN apt install -y wget curl build-essential \
       gettext git redis gunicorn supervisor winbind

COPY ./scripts/install_tools.sh /dockerstartup/install/
RUN bash /dockerstartup/install/install_tools.sh

# install Real Journals dependencies
RUN wine python -m pip install --upgrade pip
RUN wine python -m pip install wheel

RUN mkdir -p /var/log/supervisord;
RUN touch /var/log/supervisord/supervisord.log;
RUN touch /var/log/supervisord/celery.log;
RUN touch /var/log/supervisord/celery-error.log;
RUN touch /var/log/supervisord/gunicorn.log;
RUN touch /var/log/supervisord/gunicorn-error.log;
RUN touch /var/log/supervisord/supervisord.log;

RUN mkdir -p /var/run/supervisord;
RUN touch /var/run/supervisord/supervisord.pid;

RUN chmod -R 777 /var/log/supervisor*;
RUN chmod -R 777 /var/run;

COPY scripts/start-container.sh /usr/local/bin/start-container
COPY supervisord.conf /var/supervisord.conf
COPY cron.schedule /var/cron.schedule

RUN chmod u+x /usr/local/bin/start-container
RUN chmod 0644 /var/cron.schedule

COPY scripts/start-container.sh /usr/local/bin/start-container
# COPY scripts/vnc_startup.sh /usr/local/bin/vnc_startup
RUN chmod u+x /usr/local/bin/start-container

ENV DJANGO_SETTINGS_MODULE=realjournals.settings

WORKDIR /home/kasm-user/api

EXPOSE 8080

ENTRYPOINT ["start-container"]
# ENTRYPOINT ["vnc_startup"]
