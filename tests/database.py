from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import nltk
import csv

# Initialize Elasticsearch and SentenceTransformer
es = Elasticsearch()
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Define Elasticsearch index settings
index_settings = {
    "mappings": {
        "properties": {
            "song_name": {"type": "text"},
            "lyric": {"type": "text"},
            "embedding": {"type": "dense_vector", "dims": 384}  # Adjust dims based on your model output
        }
    }
}

# Create index
es.indices.create(index='lyrics', body=index_settings, ignore=400)  # ignore 400 already exists error

def index_lyrics_embeddings(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            song_name = row['SName']
            lyrics = row['Lyric'].lower()
            sentences = nltk.tokenize.sent_tokenize(lyrics)
            for sentence in sentences:
                embedding = model.encode([sentence])
                document = {
                    "song_name": song_name,
                    "lyric": sentence,
                    "embedding": embedding.tolist()
                }
                es.index(index='lyrics', document=document)

if __name__ == '__main__':
    index_lyrics_embeddings('../data/lyrics-toy-data1000.csv')