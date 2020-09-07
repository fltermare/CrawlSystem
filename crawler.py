#!/usr/bin/env python3
# from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List
from celery_app.tasks import crawl_chain, crawl_url
import concurrent.futures
import time

import sys

# import urllib.request


URLS = ['https://www.google.com/',
        'http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']


def get_url_list(num: int) -> List[str]:
    res = [str(i) + ".com" for i in range(num)]
    return res


# def get_random_string(length):
#     letters = string.ascii_lowercase
#     result_str = ''.join(random.choice(letters) for i in range(length))
#     return result_str


# def get_content(urls, timeout):
#     # print(len(urls))
#     data = []
#     # crawling
#     for url in urls:

#         time.sleep(1)
#         content = "content_%s_%s" % (url, get_random_string(100))
#         meta = "meta_%s_%s" % (url, get_random_string(100))

#         # packing
#         crawl_time = datetime.now()
#         index = "index-" + crawl_time.strftime("%Y-%m-%d")
#         url_data = {
#             "_index": index,
#             "_source": {
#                 "timestamp": crawl_time,
#                 "url": url,
#                 "content": content,
#                 "metadata": meta,
#             }
#         }
#         data.append(url_data)



#     push_crawl_data.delay(data)
#     return str(crawl_time)
#     # with urllib.request.urlopen(url, timeout=timeout) as conn:
#     #     data = conn.read()
#     #     soup = BeautifulSoup(data, 'html.parser')
#     #     metas = soup.find_all('meta')
#     #     return data, metas


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def submit_tasks(url_list: List[str]) -> None:

    URL_per_CHUNK = 50
    for i, urls in enumerate(chunks(url_list, URL_per_CHUNK)):
        if i > 0 and i % 100 == 0:
            time.sleep(URL_per_CHUNK - 5)
        crawl_chain.delay(urls)


    # with ThreadPoolExecutor(max_workers=100) as executor:
    #     future_to_url = {executor.submit(get_content, urls, 60) for urls in chunks(url_list, 50)}
    #     for future in concurrent.futures.as_completed(future_to_url):
    #         # url = future_to_url[future]
    #         try:
    #             push_time = future.result()
    #             print("[Done] %s" % push_time)
    #         except Exception as exc:
    #             print("[Exception] %s" % (exc))


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
