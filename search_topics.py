from pymongo import MongoClient

def search_topics(uri, db_name, collection_name, keyword, limit=20):
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        query = {"book_name": {"$regex": keyword, "$options": "i"}}  # Case-insensitive search
        results = collection.find(query).limit(limit)
        print(f"First {limit} books with topics containing '{keyword}':")
        for result in results:
            print(result.get('book_name'))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    uri = "mongodb://192.168.4.106:27017/"
    db_name = "oreilly"
    collection_name = "book"
    keyword = "Digital"  # Replace with your keyword
    search_topics(uri, db_name, collection_name, keyword)
