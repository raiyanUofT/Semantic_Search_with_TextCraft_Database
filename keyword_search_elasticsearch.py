from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

def keyword_search(query, index="books", fields=["book_name", "topics"], top_n=10):
    search_query = {
        "size": top_n,
        "query": {
            "multi_match": {
                "query": query,
                "fields": fields
            }
        }
    }
    
    response = es.search(index=index, body=search_query)
    results = [(hit['_source']['book_name'], hit['_source']['topics'], hit['_score']) for hit in response['hits']['hits']]
    
    return results

if __name__ == "__main__":
    query = "User"
    top_books = keyword_search(query)
    print("Top books:")
    for book, topic, score in top_books:
        print(f"Book: {book}, Topic: {topic}, Score: {score}")
