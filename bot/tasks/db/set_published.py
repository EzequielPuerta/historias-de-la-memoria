import os
from logger import logger
from pymongo import MongoClient
from datetime import datetime


def set_as_published(victim_id: str, date: datetime) -> None:
    mongo_uri = os.getenv('MONGO_DB_URI')
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client[os.getenv('MONGO_DB_DATABASE')]
    collection = db['published']

    day = date.day
    month = date.month
    existing_document = collection.find_one({'day': day, 'month': month})

    try:
        if existing_document:
            updated_victims = list(set(existing_document['desaparecidos'] + [victim_id]))
            collection.update_one(
                {'_id': existing_document['_id']},
                {'$set': {'desaparecidos': updated_victims}}
            )
            logger.debug(f"Document updated: {existing_document['_id']} with new victims.")
        else:
            document = {
                '_id': str(datetime.now().timestamp()),
                'day': day,
                'month': month,
                'desaparecidos': [victim_id]
            }
            collection.insert_one(document)
            logger.debug(f"Document inserted: {document}")
    except Exception as error:
        logger.error(f"Error inserting document: {error}")
