#!/usr/bin/env python3
# from bs4 import BeautifulSoup
# from concurrent.futures import ThreadPoolExecutor
# from datetime import datetime
from typing import List
from celery_app.tasks import crawl
# import concurrent.futures
import time
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
#     # print("Random string of length", length, "is:", result_str)
#     return result_str


# def get_content(urls, timeout):

#     data = []
#     # crawling
#     for url in urls:
#         time.sleep(1)
#         data = "data_%s_%s" % (url, get_random_string(10))
#         meta = "meta_%s_%s" % (url, get_random_string(10))

#         # packing
#         crawl_time = datetime.now()
#         index = "index-" + crawl_time.strftime("%Y-%m-%d")
#         url_data = {
#             "_index": index,
#             "crawling time": str(crawl_time),
#             "url": url,
#             "content": data,
#             "metadata": meta,
#         }
#         data.append(url_data)


#     # print(curr_time, data, meta)
#     push.delay(data)
#     print(r.task_id)

#     return data, meta
    # with urllib.request.urlopen(url, timeout=timeout) as conn:
    #     data = conn.read()
    #     soup = BeautifulSoup(data, 'html.parser')
    #     metas = soup.find_all('meta')
    #     return data, metas


def submit_tasks(url_list: List[str]) -> None:

    for url in url_list:
        crawl.delay(url)
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     future_to_url = {executor.submit(get_content, url, 60): url for url in url_list}
    #     for future in concurrent.futures.as_completed(future_to_url):
    #         url = future_to_url[future]
    #         try:
    #             data, meta = future.result()
    #         except Exception as exc:
    #             print("[Exception] %s for %s" % (exc, url))


def main():
    url_list = get_url_list(100)
    submit_tasks(url_list)


if __name__ == "__main__":
    main()
