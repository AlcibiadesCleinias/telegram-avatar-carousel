FROM python:3.9.6

WORKDIR /opt/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Layer for system requirements.
RUN apt-get update \
     && apt-get -y install gcc libpq-dev python3-dev netcat git \
     && apt-get clean \
     && rm -rf /var/lib/apt/lists/*

# Layer for Python requirements.
COPY ./core/requirements.txt .
COPY ./core/requirements-server.txt .
COPY ./core/requirements-testing.txt .
RUN pip install --upgrade pip \
     && pip install -r requirements.txt \
     && pip install -r requirements-server.txt \
     && pip install -r requirements-testing.txt \
     && pip cache purge

COPY ./.flake8 .
COPY ./.pre-commit-config.yaml .
COPY ./core .
COPY ./core/django.entrypoint.sh .

ENTRYPOINT ["/opt/src/django.entrypoint.sh"]
