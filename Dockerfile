FROM python:3.11-alpine
LABEL maintainer="ababeduguma27@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies first
RUN apk update && \
    apk add --no-cache bash shadow postgresql-client && \
    apk add --no-cache --virtual .tmp-build-deps build-base postgresql-dev musl-dev zlib-dev jpeg-dev

# Create virtual environment and install Python packages
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

# Copy source code
COPY . .

# Set PATH and run Django commands
ENV PATH="/py/bin:$PATH"

RUN python manage.py collectstatic --noinput && \
    python manage.py migrate --check

# Create django user
RUN addgroup -g 1000 django && \
    adduser -D -s /bin/bash -u 1000 -G django django && \
    chown -R django:django /app

USER django

EXPOSE 8000
