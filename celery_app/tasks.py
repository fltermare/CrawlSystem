import time
import random
import string
from celery import chain
from celery_app import app
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch, helpers

# @app.task
# def add(x, y):
#     return x + y


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)
    return result_str


@app.task(ignore_result=True)
def crawl(url):
    # crawling
    time.sleep(1)
    data = "data_%s_%s" % (url, get_random_string(10))
    meta = "meta_%s_%s" % (url, get_random_string(10))

    # packing
    crawl_time = datetime.now()
    index = "index-" + crawl_time.strftime("%Y-%m-%d")
    data = {"crawling time": str(crawl_time),
            "url": url,
            "content": data,
            "metadata": meta,
            }

    es = Elasticsearch(['http://elastic:changeme@elasticsearch:9200'])
    res = es.index(index=index, body=data)

    return len(meta), len(data), url


@app.task
def cleanup():
    curr = datetime.now()
    removed_day = curr - timedelta(days=0)
    index = "index-" + removed_day.strftime("%Y-%m-%d")
    es = Elasticsearch(['http://elastic:changeme@elasticsearch:9200'])
    es.indices.delete(index=index, ignore=[400, 404])
    return 


'''
ref. http://docs.celeryq.org/en/latest/userguide/tasks.html#avoid-launching-synchronous-subtasks
'''


# def chain_demo(x, y):
#     # add_demo ->  mul_demo -> insert_db_demo
#     chain(add_demo.s(x, y), mul_demo.s(10), insert_db_demo.s())()


# @app.task
# def add_demo(x, y):
#     time.sleep(3)
#     return x + y


# @app.task
# def mul_demo(x, y):
#     time.sleep(3)
#     return x * y


# @app.task(ignore_result=True)
# def insert_db_demo(result):
#     print('insert db , result {}'.format(result))
