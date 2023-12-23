import csv
import nltk
import time
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer

nltk.download('punkt')
nltk.download('wordnet')

def generate_lyrics_embeddings(filename):
    lemmatizer = WordNetLemmatizer()
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lyrics = row['Lyric'].lower()  # Convert to lowercase
            sentences = nltk.tokenize.sent_tokenize(lyrics)

            for sentence in sentences:
                words = nltk.tokenize.word_tokenize(sentence)
                lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
                normalized_sentence = " ".join(lemmatized_words)

                # Generate embeddings
                start = time.time()
                embedding = model.encode([normalized_sentence])
                end = time.time()

                print(f"Embedding generated in {end - start:.4f} seconds for sentence: {normalized_sentence}")
                print(embedding)
                print(embedding.shape)
                print("\n")
if __name__ == '__main__':
    generate_lyrics_embeddings('../sample-data/lyrics-toy-data1000.csv')
