from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Initialize SentenceTransformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def get_embedding(query):
    return model.encode(query).tolist()

def semantic_search(query, index="books", top_n=10):
    query_vector = get_embedding(query)
    
    # Elasticsearch query to find similar vectors
    search_query = {
        "size": top_n,
        "query": {
            "script_score": {
                "query": {
                    "match_all": {}
                },
                "script": {
                    "source": """
                        double bookNameScore = cosineSimilarity(params.query_vector, 'book_name_vector');
                        double topicsScore = cosineSimilarity(params.query_vector, 'topics_vector');
                        return (bookNameScore + topicsScore) / 2 + 1.0;
                    """,
                    "params": {
                        "query_vector": query_vector
                    }
                }
            }
        }
    }
    
    try:
        response = es.search(index=index, body=search_query)
        results = [(hit['_source']['book_name'], hit['_source']['topics'], hit['_score']) for hit in response['hits']['hits']]
        return results
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    query = "Computer"
    top_books = semantic_search(query)
    print("Top books:")
    for book, topic, score in top_books:
        print(f"Book: {book}, Topic: {topic}, Score: {score}")
