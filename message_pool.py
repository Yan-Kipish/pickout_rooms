import os
import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient(os.environ.get('MONGO_DB_URI') or "//127.0.0.1:27017")
db = client.get_database('pickout_message_pool')
pool = db.message_pool

# TODO: link to orm models (how to get room and owner metadata?)

def push_message_to_pool(message: dict):
    if message is not None:
        return pool.insert_one(message).inserted_id          
    else:
        raise Exception("Nothing to save, because message is None")

def read_messages_from_pool(room_id, owner_id=None):
    message_params = {"room_id": room_id}
    if owner_id is not None:
        message_params.update({"owner_id": owner_id})
    
    return list(pool.find(message_params))

def delete_message_from_pool(message_id=None):
    if message_id is not None:
        return pool.delete_one({"_id": ObjectId(message_id)}).deleted_count
    else:
        raise Exception("Nothing to delete, because message_id is None")
