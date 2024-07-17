from pymongo import MongoClient

def search_and_filter_topics(uri, db_name, collection_name, keyword, search_limit=200, result_limit=10):
    try:
        client = MongoClient(uri)
        db = client[db_name]
        collection = db[collection_name]
        query = {"book_name": {"$regex": keyword, "$options": "i"}}  # Case-insensitive search
        # Retrieve the first 200 documents that match the query
        results = collection.find(query).limit(search_limit)
        # Sort results by book_name (ascending order) and then limit to the top 10
        sorted_results = sorted(results, key=lambda x: x.get('book_name', ''))[:result_limit]
        print(f"Top {result_limit} books with book_names containing '{keyword}' out of the first {search_limit} hits:")
        for result in sorted_results:
            print(result.get('book_name'))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    uri = "mongodb://192.168.4.106:27017/"
    db_name = "oreilly"
    collection_name = "book"
    keyword = "Digital"  # Replace with your keyword
    search_and_filter_topics(uri, db_name, collection_name, keyword)
