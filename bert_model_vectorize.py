from pymongo import MongoClient
from transformers import BertModel, BertTokenizer
import torch

# Initialize MongoDB client
mongo_uri = "mongodb://192.168.4.106:27017/"
mongo_client = MongoClient(mongo_uri)
db = mongo_client['oreilly']
collection = db['book']

# Initialize BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

def text_to_vector(text):
    inputs = tokenizer(text, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy().tolist()[0]

def vectorize_and_store(sample_limit=200):
    count = 0
    for doc in collection.find().limit(sample_limit):
        if 'book_name' in doc:
            vector = text_to_vector(doc['book_name'])
            collection.update_one({'_id': doc['_id']}, {'$set': {'vector': vector}})
            count += 1
            print(f"Updated document {doc['_id']} with vector.")
            if count >= sample_limit:
                break

if __name__ == "__main__":
    vectorize_and_store(sample_limit=200)
