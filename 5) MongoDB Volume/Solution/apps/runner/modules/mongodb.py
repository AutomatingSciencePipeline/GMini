import sys
import pymongo

from pymongo.errors import ConnectionFailure
from modules.utils import _get_env

ENV_MONGODB_USERNAME = "MONGODB_USERNAME"
ENV_MONGODB_PASSWORD = "MONGODB_PASSWORD"

mongoClient = pymongo.MongoClient(
    "gmini-mongodb:27017",
    username=_get_env(ENV_MONGODB_USERNAME),
    password=_get_env(ENV_MONGODB_PASSWORD),
    authMechanism='SCRAM-SHA-256',
    serverSelectionTimeoutMS=1000
)
mongoGladosDB = mongoClient["gladosdb"]
    
def verify_mongo_connection():
    global mongoClient
    try:
        mongoClient.admin.command('ping')
    except ConnectionFailure as err:
        print(err, file=sys.stderr)