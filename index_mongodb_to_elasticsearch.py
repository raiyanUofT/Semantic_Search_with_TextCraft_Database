from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer

# Initialize MongoDB client
mongo_uri = "mongodb://192.168.4.106:27017/"
mongo_client = MongoClient(mongo_uri)
db = mongo_client['oreilly_subset']
collection = db['book']

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Initialize SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def create_index_with_mappings(index_name="books"):
    mappings = {
        "mappings": {
            "properties": {
                "book_name_vector": {
                    "type": "dense_vector",
                    "dims": 384  # Number of dimensions for the MiniLM embeddings
                },
                "topics_vector": {
                    "type": "dense_vector",
                    "dims": 384  # Number of dimensions for the MiniLM embeddings
                }
            }
        }
    }

    # Delete the index if it already exists
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)

    # Create the index with the defined mappings
    es.indices.create(index=index_name, body=mappings)
    print(f"Index '{index_name}' created with mappings.")

def get_embedding(text):
    return model.encode(text).tolist()

def fetch_documents_from_mongodb():
    documents = []
    for doc in collection.find():
        doc_id = str(doc['_id'])
        book_name = doc.get("book_name", "")
        topics = doc.get("topics", "")
        book_name_vector = get_embedding(book_name)
        topics_vector = get_embedding(topics)
        
        documents.append({
            "_index": "books",
            "_id": doc_id,
            "_source": {
                "book_name": book_name,
                "topics": topics,
                "book_name_vector": book_name_vector,
                "topics_vector": topics_vector
            }
        })
    return documents

def index_documents_to_elasticsearch(documents):
    try:
        helpers.bulk(es, documents)
        print(f"Successfully indexed {len(documents)} documents to Elasticsearch.")
    except Exception as e:
        print(f"Error indexing documents: {e}")

if __name__ == "__main__":
    # Step 1: Create the index with mappings
    create_index_with_mappings()

    # Step 2: Fetch documents from MongoDB and index them into Elasticsearch
    documents = fetch_documents_from_mongodb()
    index_documents_to_elasticsearch(documents)