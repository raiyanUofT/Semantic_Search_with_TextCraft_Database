from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Initialize MongoDB client
mongo_uri = "mongodb://192.168.4.106:27017/"
mongo_client = MongoClient(mongo_uri)
db = mongo_client['oreilly_subset']
collection = db['book']

# Initialize SentenceTransformer model
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

def text_to_vector(text):
    return model.encode(text).reshape(1, -1)

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
    query = "User Design"
    query_vector = text_to_vector(query)
    vectors, book_names = load_vectors_from_mongodb()
    top_books = search_books(query_vector, vectors, book_names, top_n=10)
    print("Top books:")
    for book in top_books:
        print(book)


########################

# Top books for query "Digital Transformation":

# Hacker Culture A to Z
# Planned Change
# From Data To Profit
# Mastering Bitcoin, 3rd Edition
# UX for Business
# Data Science: The Hard Parts
# Security in Computing, 6th Edition
# Inside Cyber Warfare, 3rd Edition
# Animated Realism
# Dive Into Data Science

########################

# Top books for query "Kitchen":

# Go Cookbook
# The Art Playroom
# Tidy First?
# Clean Code Cookbook
# Kafka Connect
# Machine Learning with Python Cookbook, 2nd Edition
# Acting for the Stage
# Kubernetes Cookbook, 2nd Edition
# Terraform Cookbook
# Mastering Bitcoin, 3rd Edition

########################