FROM python:3.11-alpine
LABEL maintainer="ababeduguma27@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN apk update && \
    apk add --no-cache bash shadow postgresql-client && \
    apk add --no-cache --virtual .tmp-build-deps build-base postgresql-dev musl-dev zlib-dev jpeg-dev && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps

COPY . .

# Set PATH before running Django commands
ENV PATH="/py/bin:$PATH"

RUN /py/bin/python manage.py collectstatic --noinput

RUN groupadd -r django-group && \
    useradd \
        --no-log-init \
        --create-home \
        --shell /bin/bash \
        --gid django-group \
        django-user

RUN chown -R django-user:django-group /app

USER django-user

EXPOSE 8000
