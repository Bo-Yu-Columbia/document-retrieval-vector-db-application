from elasticsearch import Elasticsearch

es = Elasticsearch(
    hosts=["http://localhost:9200"]
)
result = es.indices.create(index='news', ignore=400)

print(result)

result = es.indices.delete(index='news', ignore=[400, 404])
print(result)