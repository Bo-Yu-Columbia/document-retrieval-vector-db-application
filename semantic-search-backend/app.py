from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import graphene
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from flask_graphql import GraphQLView
from dotenv import load_dotenv
import os
from helper import encode_image_to_base64, process_image_with_openai
import requests
import base64

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')

# Initialize Elasticsearch and SentenceTransformer
es = Elasticsearch(hosts=["http://localhost:9200"])
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')


def standard_lyrics_search(query):
    response = es.search(index="lyrics-all", query={"match": {"lyric": query}})
    return [
        SearchResult(
            song_name=hit['_source']['song_name'],
            lyric=hit['_source']['lyric'],
            score=None  # Score is not applicable for standard search
        ) for hit in response['hits']['hits']
    ]


def image_lyrics_search(query):
    query_embedding = model.encode([query.lower()]).tolist()[0]

    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                "params": {"query_vector": query_embedding}
            }
        },
    }

    response = es.search(index="lyrics-all", body={"query": script_query}, size=10)
    results = []

    for hit in response['hits']['hits']:
        result = SearchResult(
            song_name=hit['_source']['song_name'],
            lyric=hit['_source']['lyric'],
            score=hit['_score'],
            singer=hit['_source'].get('singer', 'Unknown')  # Adjust based on your data
        )
        results.append(result)

        # Print each result
        print("Song Name:", result.song_name)
        print("Lyric:", result.lyric)
        print("Score:", result.score)
        print("Singer:", result.singer)
        print("-" * 50)  # Separator for readability

    return results


class SearchResult(graphene.ObjectType):
    song_name = graphene.String()
    lyric = graphene.String()
    score = graphene.Float()
    singer = graphene.String()  # Add this if you have singer information


class Query(graphene.ObjectType):
    semantic_lyrics_search = graphene.List(SearchResult, query=graphene.String())
    standard_lyrics_search = graphene.List(SearchResult, query=graphene.String())
    image_lyrics_search = graphene.List(SearchResult, query=graphene.String())

    def resolve_semantic_lyrics_search(self, info, query):
        query_embedding = model.encode([query.lower()]).tolist()[0]
        print("embbeding: ", query_embedding)
        print("first dim: ", query_embedding[0])
        print("shape: ", len(query_embedding))

        script_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_embedding}
                }
            },

            # # Manhattan Distance
            # "script_score": {
            #     "script": {
            #         "source": "params.query_vector.stream().mapToDouble((x, i) -> Math.abs(x - doc["
            #                   "'embedding_vector'][i])).sum()",
            #         "params": {"query_vector": query_embedding}
            #     }
            # },

            # Euclidean Distance
            # "script_score": {
            #     "script": {
            #         "source": """
            #         if (doc['embedding_vector'].empty) {
            #             return 0;
            #         }
            #         double sum = 0;
            #         for (int i = 0; i < params.query_vector.length; i++) {
            #             sum += Math.pow(params.query_vector[i] - (doc['embedding_vector'].size() > i ? doc['embedding_vector'][i] : 0), 2);
            #         }
            #         return Math.sqrt(sum);
            #         """,
            #         "params": {"query_vector": query_embedding}
            #     }
            # }
        }

        response = es.search(index="lyrics-all", body={"query": script_query}, size=10)
        results = []

        for hit in response['hits']['hits']:
            result = SearchResult(
                song_name=hit['_source']['song_name'],
                lyric=hit['_source']['lyric'],
                score=hit['_score'],
                singer=hit['_source'].get('singer', 'Unknown')  # Adjust based on your data
            )
            results.append(result)

            # Print each result
            print("Song Name:", result.song_name)
            print("Lyric:", result.lyric)
            print("Score:", result.score)
            print("Singer:", result.singer)
            print("-" * 50)  # Separator for readability

        return results

    def resolve_standard_lyrics_search(self, info, query):
        return standard_lyrics_search(query)

    # def resolve_image_lyrics_search(self, info, query):
    #     return image_lyrics_search(query)


schema = graphene.Schema(query=Query)

app = Flask(__name__)
CORS(app, resources={r"/graphql/*": {"origins": "http://localhost:3000"}})
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()


@app.before_request
def log_request():
    if request.path == '/graphql':
        print("Received GraphQL Request:", request.json)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    base64_image = encode_image_to_base64(file)
    extracted_text = process_image_with_openai(base64_image)
    print("Extracted Text:", extracted_text)
    search_results = image_lyrics_search(extracted_text)
    print("Search Results:", search_results)
    return search_results


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
