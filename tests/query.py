from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import nltk

# Initialize Elasticsearch and SentenceTransformer
es = Elasticsearch()
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def standard_lyrics_search(query):
    # Elasticsearch query for standard text search
    response = es.search(index="lyrics", query={"match": {"lyric": query}})
    return [(hit['_source']['song_name'], hit['_source']['lyric']) for hit in response['hits']['hits']]

def semantic_lyrics_search(query):
    # Process the query
    query_embedding = model.encode([query.lower()])

    # Elasticsearch query for semantic search
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                "params": {"query_vector": query_embedding.tolist()}
            }
        }
    }

    response = es.search(index="lyrics", body={"query": script_query}, size=10)
    return [(hit['_source']['song_name'], hit['_source']['lyric'], hit['_score']) for hit in response['hits']['hits']]

# Example usage
text_query = "love and life"
print("Standard Search Results:")
for song, lyric in standard_lyrics_search(text_query):
    print(f"Song: {song}, Lyric: {lyric}")

print("\nSemantic Search Results:")
for song, lyric, score in semantic_lyrics_search(text_query):
    print(f"Song: {song}, Lyric: {lyric}, Score: {score}")
