from pymongo import MongoClient

# Initialize MongoDB client
mongo_uri = "mongodb://192.168.4.106:27017/"
mongo_client = MongoClient(mongo_uri)
db = mongo_client['oreilly']
collection = db['book']

def fetch_first_200_books():
    books = []
    for doc in collection.find().limit(200):
        if 'book_name' in doc:
            books.append(doc['book_name'])
    return books

def save_to_file(book_names, filename="first_200_books.txt"):
    with open(filename, 'w') as file:
        for book in book_names:
            file.write(f"{book}\n")

if __name__ == "__main__":
    first_200_books = fetch_first_200_books()
    print("First 200 books:")
    for book in first_200_books:
        print(book)
    save_to_file(first_200_books)
    print(f"First 200 book names saved to first_200_books.txt")
