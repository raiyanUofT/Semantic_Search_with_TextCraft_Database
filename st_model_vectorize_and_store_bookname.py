from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize MongoDB client
mongo_uri = "mongodb://192.168.4.106:27017/"
mongo_client = MongoClient(mongo_uri)
db = mongo_client['oreilly']
collection = db['book']

# Initialize SentenceTransformer model
model_name = 'sentence-transformers/all-MiniLM-L6-v2'
model = SentenceTransformer(model_name)

def text_to_vector(text):
    return model.encode(text).tolist()

def vectorize_and_store(sample_limit=200):
    # Remove existing embeddings
    collection.update_many({}, {'$unset': {'vector': ''}})
    
    count = 0
    for doc in collection.find().limit(sample_limit):
        if 'book_name' in doc:
            vector = text_to_vector(doc['book_name'])
            collection.update_one({'_id': doc['_id']}, {'$set': {'vector': vector}})
            count += 1
            print(f"Updated document {doc['_id']} with vector.")
            if count >= sample_limit:
                break

if __name__ == "__main__":
    vectorize_and_store(sample_limit=200)
