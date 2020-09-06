import time
from celery import chain
from celery_app import app
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch, helpers

# @app.task
# def add(x, y):
#     return x + y


@app.task(ignore_result=True)
def push_crawl_data(data):
    time.sleep(1)
    es = Elasticsearch(['http://elastic:changeme@elasticsearch:9200'])
    # res = es.index(index=index, body=data)
    helpers.bulk(es, data)

    return len(data)


@app.task
def cleanup():
    curr = datetime.now()
    removed_day = curr - timedelta(days=30)
    index = "index-" + removed_day.strftime("%Y-%m-%d")
    es = Elasticsearch(['http://elastic:changeme@elasticsearch:9200'])
    es.indices.delete(index=index, ignore=[400, 404])
    return 



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
