from pymongo import MongoClient
from elasticsearch import Elasticsearch, helpers
from bs4 import BeautifulSoup
import zlib
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize MongoDB client
mongo_uri = "mongodb://192.168.4.106:27017/"
mongo_client = MongoClient(mongo_uri)
mogo = mongo_client['oreilly_subset']
collection = mogo['book']

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

def mongo2ES():
    logger.info("Running mongo2ES...")
    try:
        logger.info(es.info())
    except Exception as e:
        logger.error(f"Failed to connect to Elasticsearch: {e}")
        return

    try:
        books_mogon = mogo['book'].find({"user": {"$exists": False}})
    except Exception as e:
        logger.error(f"Failed to fetch data from MongoDB: {e}")
        return

    for book in books_mogon:
        if 'book_name' not in book:
            continue

        book['chaptersContent'] = [cc for cc in book['chaptersContent'] if cc]

        if len(book['allChapters']) > 1 and len(book['allChapters']) == len(book['chaptersContent']):
            logger.info(f"Processing book: {book['archive_id']}")
            actions = []
            newChaptersContent = []

            for cc in book['chaptersContent']:
                if 'isZip' in cc and cc['isZip'] == "Y":
                    cc['content'] = zlib.decompress(cc['content'])

                soup = BeautifulSoup(cc['content'], 'html.parser')
                cc['content'] = str(soup)

                # Data to be written into ES
                cid = f"{book['archive_id']}_{cc['idx']}"
                doc = {
                    "book_name": book['book_name'],
                    "topics": book['topics'],
                    "idx": cc['idx'],
                    "title": cc['title'],
                    "archive_id": book['archive_id'],
                    "content": cc['content'],
                }
                actions.append({
                    "_index": "book_chapter",  # The index name is specified here
                    "_id": cid,
                    "_source": doc
                })

                # Update data in MongoDB
                cc['content'] = zlib.compress(cc['content'].encode('utf-8'))
                cc['isZip'] = "Y"
                newChaptersContent.append(cc)

            try:
                # Update MongoDB
                resp = mogo['book'].update_one(
                    {"archive_id": book['archive_id']},
                    {"$set": {"chaptersContent": newChaptersContent}}
                )
                logger.info(f"Update MongoDB: {resp.raw_result}")

                # Write to ES
                resp = helpers.bulk(es, actions)
                logger.info(f"Indexed {resp[0]} documents into Elasticsearch")

                mogo['book'].update_one(
                    {"archive_id": book['archive_id']},
                    {'$set': {"ESindex": datetime.now().strftime("%Y-%m-%d")}}
                )
            except Exception as e:
                logger.error(f"Failed to process book {book['archive_id']}: {e}")

mongo2ES()
