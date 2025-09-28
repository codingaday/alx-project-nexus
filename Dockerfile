FROM python:3.11-alpine
LABEL maintainer="ababeduguma27@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# System deps
RUN apk update && \
    apk add --no-cache bash shadow postgresql-client && \
    apk add --no-cache --virtual .tmp-build-deps build-base postgresql-dev musl-dev zlib-dev jpeg-dev

# Create virtual environment
RUN python -m venv /py
ENV PATH="/py/bin:$PATH"

# Upgrade pip inside venv
RUN /py/bin/python -m pip install --upgrade pip setuptools wheel

# Install Python deps
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
RUN /py/bin/python -m pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/python -m pip install -r /tmp/requirements.dev.txt; fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

# Copy project
COPY . .

# Collect static + migrate
RUN /py/bin/python manage.py collectstatic --noinput --clear && \
    /py/bin/python manage.py migrate --run-syncdb

# Django user
RUN addgroup -g 1000 django && \
    adduser -D -s /bin/bash -u 1000 -G django django && \
    chown -R django:django /app

USER django

EXPOSE 8000
