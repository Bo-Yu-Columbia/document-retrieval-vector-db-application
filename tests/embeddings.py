from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Sentences we want to encode. Example:
sentence = ['This framework generates embeddings for each input sentence']

# Sentences are encoded by calling model.encode()
embedding = model.encode(sentence)
print(embedding.shape)

sentence2 = ['This is another sentence.']
import time
start = time.time()
embedding2 = model.encode(sentence2)
end = time.time()
print(end - start, "seconds")
print(embedding2.shape)
print(embedding2)