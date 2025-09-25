FROM python:3.13-slim-bookworm
ARG REQUESTS_CA_BUNDLE
LABEL maintainer="synthetiqsignals.com" \
    org.label-schema.docker.dockerfile="/Dockerfile" \
    org.label-schema.name="Pingblender" 

#python variable settings for image set
ENV PYTHONPATH="/app/signals/" \
    PYTHONDONTWITEBYTECODE=1 \
    PYTHONBUFFERED=1 \
    REQUESTS_CA_BUNDLE=${REQUESTS_CA_BUNDLE}

#handle cert placement explicitly
COPY ${REQUESTS_CA_BUNDLE} /etc/docker/certs.d/

WORKDIR /app/

#copy directory to /app/
COPY . . 
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y gcc git ca-certificates \
    && update-ca-certificates \
    && apt-get install -y build-essential \
    #testing build
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#ready NodeJS for image interface.
# RUN apt-get update && apt-get install -y \
#      software-properties-common \
#      npm

#set policy for access to entrypoint.sh
WORKDIR /app/signals/
RUN chmod +x entrypoint.sh

#create a virtual environment to run in closed unit
WORKDIR /app
RUN python -m venv /venv
RUN /venv/bin/python -m pip install --upgrade pip
RUN /venv/bin/pip install -r requirements.txt

EXPOSE 1010 5432 5678

#access entrypoint as intended.
ENTRYPOINT [ "/app/signals/entrypoint.sh" ]