from pymongo import MongoClient

def test_mongodb_connection(uri):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Attempt to get server info to verify connection
        server_info = client.server_info()
        print("Connected to MongoDB, server info:")
        print(server_info)
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    # Use the actual IP address found in ipconfig
    uri = "mongodb://192.168.4.106:27017/"
    test_mongodb_connection(uri)

