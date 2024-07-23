from pymongo import MongoClient

# Initialize MongoDB clients
source_mongo_uri = "mongodb://192.168.4.106:27017/"
destination_mongo_uri = "mongodb://192.168.4.106:27017/"

source_client = MongoClient(source_mongo_uri)
destination_client = MongoClient(destination_mongo_uri)

source_db = source_client['oreilly']
source_collection = source_db['book']

destination_db = destination_client['oreilly_subset']
destination_collection = destination_db['book']

def clear_collection():
    result = destination_collection.delete_many({})
    print(f"Cleared {result.deleted_count} documents from 'oreilly_subset.book' collection.")

def extract_and_insert(sample_limit=200):
    documents = source_collection.find().limit(sample_limit)
    docs_to_insert = []
    for doc in documents:
        # Copy the original '_id' to a new field 'original_id'
        original_id = doc['_id']
        doc['original_id'] = original_id
        # Remove the '_id' field to avoid duplicate key error in the new collection
        doc.pop('_id', None)
        docs_to_insert.append(doc)
    
    if docs_to_insert:
        destination_collection.insert_many(docs_to_insert)
        print(f"Inserted {len(docs_to_insert)} documents into the 'oreilly_subset' database.")

if __name__ == "__main__":
    clear_collection()
    extract_and_insert(sample_limit=200)
