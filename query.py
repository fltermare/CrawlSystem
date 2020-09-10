from datetime import datetime
from elasticsearch import Elasticsearch, helpers

domain_param = {"query": {"match_phrase": {"domain": "99.com"}}}

url_param = {"query": {"match_phrase": {"url": "99.com/100/101"}}}

# search2_param = {
#     "query": {
#         "terms": {
#             "url": ["com"]
#         }
#     }
# }

# search3_param = {
#     "query": {
#         "wildcard": {
#             "metadata": "*hvbfljzy*"
#         }
#     }
# }

# search4_param = {
#     "query": {
#         "regexp": {
#             "metadata": ".*hvbfljzy.*"
#         }
#     }
# }

# search5_param = {
#     "query": {
#         "regexp": {
#             "url": "1[0-9].com"
#         }
#     }
# }

match_all_param = {"size": 100000, "query": {"match_all": {}}}

es = Elasticsearch(["http://elastic:changeme@elasticsearch:9200"])

for param in [url_param, domain_param]:

    res = es.search(index="index-*", body=param, scroll="3m")
    for i, doc in enumerate(res["hits"]["hits"], 1):
        print(i, doc)

# scroll_id = res['_scroll_id']
# res = es.scroll(
#     scroll_id = scroll_id,
#     scroll = '3s', # time value for search
# )

# print ('scroll() query length:', len(res))

res = helpers.scan(
    es,
    query=match_all_param,
    scroll="3m",
    size=1000,
    index="index-*",
)

# returns a generator object
print(type(res))
data = [doc for num, doc in enumerate(res)]
for num, doc in enumerate(data):
    print(num, doc)

print("\nscan() scroll length:", len(data))


# update document
updated_body = {
    "doc": {
        "content": "content_9698.com/9699/9700_5566neverdie",
        "new": "new_column"
    }
}

es.update(index="index-2020-09-09", id="thwNcXQB6YV2zoLgOMzW", doc_type="_doc", body=updated_body)


# helpers.reindex(
#     es,
#     source_index="index-2020-09-08",
#     target_index="index-2020-09-06"
# )

# helpers.reindex(
#     es,
#     source_index="index-2020-09-08",
#     target_index="index-2020-09-05",
#     query=search_param,
# )
