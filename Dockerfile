FROM python:3.6.9
LABEL maintainer twtrubiks
ENV PYTHONUNBUFFERED 1
RUN mkdir /celery_app
WORKDIR /celery_app
COPY . /celery_app/
RUN pip install -r requirements.txt
