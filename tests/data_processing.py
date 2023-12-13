# import csv
# import nltk
# nltk.download('punkt')
#
# def tokenize_lyrics(filename):
#     with open(filename, 'r', encoding='utf-8') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             lyrics = row['Lyric']
#             sentences = nltk.tokenize.sent_tokenize(lyrics)
#             print(f"Song: {row['SName']}")
#             for sentence in sentences:
#                 print(sentence)
#             print("\n")
# Usage example
# tokenize_lyrics('../data/lyrics-toy-data1000.csv')


import csv
import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

def normalize_and_tokenize_lyrics(filename):
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lyrics = row['Lyric'].lower()  # Convert to lowercase
            sentences = nltk.tokenize.sent_tokenize(lyrics)

            for sentence in sentences:
                words = nltk.tokenize.word_tokenize(sentence)
                stemmed_words = [stemmer.stem(word) for word in words]
                lemmatized_words = [lemmatizer.lemmatize(word) for word in words]

                # Choose whether to use stemmed or lemmatized words here
                normalized_words = stemmed_words

                print(" ".join(normalized_words))

if __name__ == '__main__':
    normalize_and_tokenize_lyrics('../data/lyrics-toy-data1000.csv')


