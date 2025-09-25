FROM python:3.11-alpine
LABEL maintainer="ababeduguma27@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN apk update && \
    apk add --no-cache bash shadow

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp 

RUN groupadd -r django-group && \
    useradd \
        --no-log-init \
        --create-home \
        --shell /bin/bash \
        --gid django-group \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user
