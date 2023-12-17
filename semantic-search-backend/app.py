# # app.py
# from flask import Flask, current_app, request
# from flask_graphql import GraphQLView
# import graphene
# from elasticsearch import Elasticsearch
# from sentence_transformers import SentenceTransformer
# import nltk
# from flask_cors import CORS
# from flask import Response
#
#
# app = Flask(__name__)
# # CORS(app)
# # CORS(app, resources={r"/graphql/*": {"origins": "*"}})
# CORS(app, resources={r"/graphql/*": {"origins": "http://localhost:3000"}})
# # CORS(app, resources={r"/graphql/*": {"origins": "*", "allow_headers": ["Content-Type"]}})
# # CORS(app, resources={r"/graphql/*": {"origins": "*", "allow_headers": ["Content-Type"], "expose_headers": ["Content-Type"]}})
# # Initialize Elasticsearch and SentenceTransformer
# es = Elasticsearch(hosts=["http://localhost:9200"])
# model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
#
# class SearchResult(graphene.ObjectType):
#     song_name = graphene.String()
#     lyric = graphene.String()
#     score = graphene.Float()
#
# class Query(graphene.ObjectType):
#     semantic_lyrics_search = graphene.List(SearchResult, query=graphene.String())
#
#     def resolve_semantic_lyrics_search(self, info, query):
#         query_embedding = model.encode([query.lower()]).tolist()[0]
#
#         script_query = {
#             "script_score": {
#                 "query": {"match_all": {}},
#                 "script": {
#                     "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
#                     "params": {"query_vector": query_embedding}
#                 }
#             }
#         }
#
#         response = es.search(index="lyrics", body={"query": script_query}, size=10)
#
#         return [
#             SearchResult(
#                 song_name=hit['_source']['song_name'],
#                 lyric=hit['_source']['lyric'],
#                 score=hit['_score']
#             ) for hit in response['hits']['hits']
#         ]
#
# schema = graphene.Schema(query=Query)
#
# app = Flask(__name__)
# app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
#
# @current_app.before_request
# def basic_authentication():
#     if request.method.lower() == 'options':
#         return Response()
#
# if __name__ == '__main__':
#     app.run(debug=True)
#     # app.run()


from flask import Flask, request, Response
from flask_cors import CORS
import graphene
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from flask_graphql import GraphQLView

# Initialize Elasticsearch and SentenceTransformer
es = Elasticsearch(hosts=["http://localhost:9200"])
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

class SearchResult(graphene.ObjectType):
    song_name = graphene.String()
    lyric = graphene.String()
    score = graphene.Float()
    singer = graphene.String()  # Add this if you have singer information

class Query(graphene.ObjectType):
    semantic_lyrics_search = graphene.List(SearchResult, query=graphene.String())

    def resolve_semantic_lyrics_search(self, info, query):
        query_embedding = model.encode([query.lower()]).tolist()[0]

        script_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {"query_vector": query_embedding}
                }
            }
        }

        response = es.search(index="lyrics", body={"query": script_query}, size=10)
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

if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
