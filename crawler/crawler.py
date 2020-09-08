#!/usr/bin/env python3
import time
import sys
from typing import List
from celery_app.tasks import crawl_chain, crawl_url


def get_url_list(num: int) -> List[str]:
    res = ["{}.com/{}/{}".format(i, i+1, i+2) for i in range(num)]
    return res


def chunks(lst: List[str], n: int) -> List[str]:
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def submit_tasks(url_list: List[str]) -> None:

    URL_per_CHUNK = 50
    for i, urls in enumerate(chunks(url_list, URL_per_CHUNK)):
        if i > 0 and i % 100 == 0:
            time.sleep(URL_per_CHUNK)
        crawl_chain.delay(urls)
    time.sleep(URL_per_CHUNK)


def main():
    try:
        num = int(sys.argv[1])
    except IndexError:
        num = 1000
    start = time.time()
    url_list = get_url_list(num)
    submit_tasks(url_list)
    end = time.time()
    print("Cost %f sec for %d urls" % (end - start, num))


if __name__ == "__main__":
    main()
