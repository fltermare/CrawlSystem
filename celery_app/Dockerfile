FROM python:3.6.9
LABEL maintainer albert
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY crawler.py /app/
COPY .tld_set /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY __init__.py /app/celery_app/
COPY celery_config.py /app/celery_app/
COPY main.py /app/celery_app/
COPY tasks.py /app/celery_app/
