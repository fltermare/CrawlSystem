import time
from celery import chain
from .main import app
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch, helpers
import string
import random
import tldextract


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


@app.task(ignore_result=True)
def crawl_chain(urls):
    # crawl_url ->  push_data
    chain(crawl_url.s(urls), push_data.s())()


@app.task(ignore_result=True)
def crawl_url(urls):

    # print(len(urls))
    data = []
    # crawling
    for url in urls:

        time.sleep(1)
        content = "content_%s_%s" % (url, get_random_string(100))
        meta = "meta_%s_%s" % (url, get_random_string(100))
        extractor = tldextract.TLDExtract(cache_file=".tld_set")
        ext = extractor(url)

        # packing
        crawl_time = datetime.now()
        index = "index-" + crawl_time.strftime("%Y-%m-%d")
        url_data = {
            "_index": index,
            "_source": {
                "timestamp": crawl_time,
                "url": url,
                "content": content,
                "metadata": meta,
                "domain": ".".join([ext.domain, ext.suffix]),
            },
        }
        data.append(url_data)

    # time.sleep(1)
    # es = Elasticsearch(['http://elastic:changeme@elasticsearch:9200'])
    # helpers.bulk(es, data)
    # return len(data)
    return data


@app.task(ignore_result=True)
def push_data(data):
    time.sleep(1)
    es = Elasticsearch(["http://elastic:changeme@elasticsearch:9200"])
    # res = es.index(index=index, body=data)
    helpers.bulk(es, data)
    return len(data)


@app.task
def cleanup():
    curr = datetime.now()
    removed_day = curr - timedelta(days=30)
    index = "index-" + removed_day.strftime("%Y-%m-%d")
    es = Elasticsearch(["http://elastic:changeme@elasticsearch:9200"])
    es.indices.delete(index=index, ignore=[400, 404])
    return

# @app.task
# def add(x, y):
#     return x + y
