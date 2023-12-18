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



# df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
# df.to_csv('output/embedded_1k_reviews.csv', index=False)

import torch.nn.functional as F
from torch import Tensor
from transformers import AutoTokenizer, AutoModel

def average_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

input_texts = [
    "what is the capital of China?",
    "how to implement quick sort in python?",
    "Beijing",
    "sorting algorithms"
]

tokenizer = AutoTokenizer.from_pretrained("thenlper/gte-base")
model = AutoModel.from_pretrained("thenlper/gte-base")

# Tokenize the input texts
batch_dict = tokenizer(input_texts, max_length=512, padding=True, truncation=True, return_tensors='pt')

outputs = model(**batch_dict)
embeddings = average_pool(outputs.last_hidden_state, batch_dict['attention_mask'])

# (Optionally) normalize embeddings
embeddings = F.normalize(embeddings, p=2, dim=1)
scores = (embeddings[:1] @ embeddings[1:].T) * 100
print(scores.tolist())

from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

sentences = ['That is a happy person', 'That is a very happy person']

model = SentenceTransformer('thenlper/gte-base')
embeddings = model.encode(sentences)
print(cos_sim(embeddings[0], embeddings[1]))
