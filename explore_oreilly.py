from pymongo import MongoClient

def explore_database(uri, db_name):
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collections = db.list_collection_names()
        print(f"Collections in database '{db_name}':")
        for collection_name in collections:
            print(f" - {collection_name}")
            collection = db[collection_name]
            sample_doc = collection.find_one()
            print(f"   Sample document from '{collection_name}': {sample_doc}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    uri = "mongodb://192.168.4.106:27017/"
    db_name = "oreilly"
    explore_database(uri, db_name)
