import pymongo
from dotenv import load_dotenv
import os
import time

from helpers.logging import get_logger

logger = get_logger("upsert_logs")


def get_client():
    load_dotenv()
    db_connection_string = (
        os.environ.get("MONGODB_URL_DEV")
        if os.environ.get("ENV") == "dev"
        else os.environ.get("MONGODB_URL_PROD")
    )
    return pymongo.MongoClient(db_connection_string)


def upsert_docs_for_one_collection(collection_name, src_collection, dest_collection):
    """Performs an upsert of all documents from the source collection to the destination collection."""
    try:
        logger.info(f"==> Upserting {collection_name}")
        start = time.time()
        src_docs = list(src_collection.find({}))
        for doc in src_docs:
            dest_collection.update_one({"_id": doc["_id"]}, {"$set": doc}, upsert=True)
        end = time.time()
        time_taken = end - start
        logger.info(f"Time taken: {time_taken}s")
    except Exception as e:
        logger.error(f"Error upserting {collection_name}: {e}")


def upsert_docs_for_all_companies(collection_name, src_db, dest_db, companies):
    """Performs an upsert of all documents from the source collection to the destination collection for all companies"""
    try:
        logger.info(f"==> Upserting {collection_name}")
        start = time.time()
        for company in companies:
            src_docs = list(src_db[company][collection_name].find({}))
            for doc in src_docs:
                dest_db[collection_name].update_one(
                    {"_id": doc["_id"]}, {"$set": doc}, upsert=True
                )
        end = time.time()
        time_taken = end - start
        logger.info(f"Time taken: {time_taken}s")
    except Exception as e:
        logger.error(f"Error upserting {collection_name}: {e}")
