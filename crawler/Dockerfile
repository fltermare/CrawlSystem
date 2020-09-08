FROM python:3.6.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY crawler.py /app/
COPY .tld_set /app/
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./celery_app /app/celery_app
