
# Semantic Search with TextCraft Database

## Project Overview

This project demonstrates how to perform semantic search using Elasticsearch and sentence-transformers on a MongoDB dataset. The dataset contains book information, including `book_name` and `topics`, which are indexed into Elasticsearch with embeddings. The project includes scripts for indexing the data and performing semantic search.

## Prerequisites

- Python 3.x
- MongoDB
- Elasticsearch
- Required Python libraries:
  - `pymongo`
  - `elasticsearch`
  - `sentence-transformers`
  - `torch`

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure MongoDB and Elasticsearch are Running**:
   - MongoDB should be running and contain the dataset.
   - Elasticsearch should be running on `http://localhost:9200`.

## Project Structure

- `index_mongodb_to_elasticsearch.py`: Main script that creates the Elasticsearch index, fetches documents from MongoDB, creates embeddings, and indexes the documents into Elasticsearch

## Usage

### 1. Create and Index Data

Run the `index_mongodb_to_elasticsearch.py` script to create the index in Elasticsearch, fetch documents from MongoDB, generate embeddings using the sentence-transformers model, and index the documents into Elasticsearch.

```bash
python3 index_mongodb_to_elasticsearch.py
```

### 2. Perform Semantic Search

The script `semantic_search_elasticsearch.py` performs a semantic search on the indexed data. You can modify the `query` variable in the script to search for different terms.

### Example Output

After running the script, the output will display the top books based on the semantic search query:

```plaintext
Top books:
Book: Book Name 1, Topic: Topic 1, Score: 1.23
Book: Book Name 2, Topic: Topic 2, Score: 1.19
...
```

## Script Details

### `semantic_search_elasticsearch.py`

This script performs the following task:

1. **Perform Semantic Search**:
   - Performs a semantic search using cosine similarity between the query vector and both the `book_name_vector` and `topics_vector`.
   - Averages the similarity scores to provide a combined relevance score.

### Environment Setup

Ensure that MongoDB and Elasticsearch are set up and running:

- **MongoDB**: Ensure MongoDB is running and contains the dataset in the `oreilly_subset` database and `book` collection.
- **Elasticsearch**: Ensure Elasticsearch is running on `http://localhost:9200`.

### Dependencies

Ensure you have the required Python libraries installed:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgments

- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [Sentence-Transformers](https://www.sbert.net/)
- [PyMongo](https://pymongo.readthedocs.io/)
