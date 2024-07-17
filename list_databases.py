from pymongo import MongoClient

def list_databases(uri):
    try:
        client = MongoClient(uri)
        databases = client.list_database_names()
        print("Databases:")
        for db in databases:
            print(f" - {db}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Use the actual IP address found in ipconfig
    uri = "mongodb://192.168.4.106:27017/"
    list_databases(uri)
