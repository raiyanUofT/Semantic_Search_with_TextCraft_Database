from elasticsearch import Elasticsearch

def test_elasticsearch_connection():
    # Replace 'localhost' with the IP address if your Elasticsearch is not on the same machine
    es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

    # Test the connection
    if es.ping():
        print("Connected to Elasticsearch!")
        # Print cluster information
        print(es.info())
    else:
        print("Could not connect to Elasticsearch.")

if __name__ == "__main__":
    test_elasticsearch_connection()
