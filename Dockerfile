FROM python:3.11-alpine
LABEL maintainer="ababeduguma27@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies first
RUN apk update && \
    apk add --no-cache bash shadow postgresql-client && \
    apk add --no-cache --virtual .tmp-build-deps build-base postgresql-dev musl-dev zlib-dev jpeg-dev

# Create virtual environment FIRST
RUN python -m venv /py

# Set PATH immediately after creating venv
ENV PATH="/py/bin:$PATH"

# Upgrade pip in the virtual environment
RUN pip install --upgrade pip

# Copy requirements and install Python packages
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; \
        then pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

# Copy source code AFTER Python packages are installed
COPY . .

# Run Django management commands (now PATH is already set)
RUN python manage.py collectstatic --noinput --clear && \
    python manage.py migrate --run-syncdb

# Create django user
RUN addgroup -g 1000 django && \
    adduser -D -s /bin/bash -u 1000 -G django django && \
    chown -R django:django /app

USER django

EXPOSE 8000
