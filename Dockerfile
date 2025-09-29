FROM python:3.13-slim-bookworm
ARG REQUESTS_CA_BUNDLE
LABEL maintainer="synthetiqsignals.com" \
    org.label-schema.docker.dockerfile="/Dockerfile" \
    org.label-schema.name="Scrambler Signals Base - PYTHON 3.13-slim-bookworm" 

#python variable settings for image set
ENV PYTHONPATH=/app/signals/
ENV PYTHONDONTWITEBYTECODE=1 
ENV PYTHONBUFFERED=1 
ENV REQUESTS_CA_BUNDLE=${REQUESTS_CA_BUNDLE}

WORKDIR /app/
COPY . .

#copy directory to /app/
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y gcc git ca-certificates \
    && update-ca-certificates \
    && apt-get install -y build-essential \
    #testing build
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

#create a virtual environment to run in closed unit
WORKDIR /app/signals/
RUN python -m venv /venv
RUN /venv/bin/python -m pip install --upgrade pip
RUN /venv/bin/pip install -r requirements.txt

EXPOSE 8000 5432 7474 5678 7473 7687

#access entrypoint as intended.
ENTRYPOINT [ "/app/shell/entrypoint.sh" ]