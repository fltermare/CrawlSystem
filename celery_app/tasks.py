import time

from celery import chain

from celery_app import app
from datetime import datetime

@app.task
def add(x, y):
    return x + y


@app.task
def crawl(url):
    time.sleep(1)
    curr_time = datetime.now()
    data = "data_" + url
    meta = "meta_" + url
    return len(meta), len(data), url


'''
ref. http://docs.celeryq.org/en/latest/userguide/tasks.html#avoid-launching-synchronous-subtasks
'''


def chain_demo(x, y):
    # add_demo ->  mul_demo -> insert_db_demo
    chain(add_demo.s(x, y), mul_demo.s(10), insert_db_demo.s())()


@app.task
def add_demo(x, y):
    time.sleep(3)
    return x + y


@app.task
def mul_demo(x, y):
    time.sleep(3)
    return x * y


@app.task(ignore_result=True)
def insert_db_demo(result):
    print('insert db , result {}'.format(result))
