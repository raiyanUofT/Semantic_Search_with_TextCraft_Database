from pymongo import MongoClient
from transformers import BertModel, BertTokenizer
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Initialize MongoDB client
mongo_uri = "mongodb://192.168.4.106:27017/"
mongo_client = MongoClient(mongo_uri)
db = mongo_client['oreilly']
collection = db['book']

# Initialize BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

def text_to_vector(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

def load_vectors_from_mongodb():
    vectors = []
    book_names = []
    for doc in collection.find({'vector': {'$exists': True}}):
        vectors.append(doc['vector'])
        book_names.append(doc['book_name'])
    return np.array(vectors), book_names

def search_books(query_vector, vectors, book_names, top_n=10):
    similarities = cosine_similarity(query_vector, vectors)[0]
    top_indices = np.argsort(similarities)[-top_n:][::-1]
    return [book_names[i] for i in top_indices]

if __name__ == "__main__":
    query = "Computers"
    query_vector = text_to_vector(query)
    vectors, book_names = load_vectors_from_mongodb()
    top_books = search_books(query_vector, vectors, book_names, top_n=10)
    print("Top books:")
    for book in top_books:
        print(book)

########################################
# Top books for query "Computers":

# Practical Salesforce Architecture
# Data Science: The Hard Parts
# The Art Playroom
# Color Management for Photographers
# The LEGO Lighting Book
# Software Engineering for Data Scientists
# Machine Learning Interviews
# Hacker Culture A to Z
# Learning Modern C++ for Finance
# Learning Airtable
########################################
