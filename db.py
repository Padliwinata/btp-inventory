from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus

from settings import MONGO_DB, MONGO_PASSWORD, MONGO_USERNAME


username = quote_plus(MONGO_USERNAME)
password = quote_plus(MONGO_PASSWORD)

uri = f"mongodb+srv://{username}:{password}@btp.qxwgsej.mongodb.net/?retryWrites=true&w=majority&appName=btp"

client = MongoClient(uri)
db = client[MONGO_DB]

db_users = db['users']
db_roles = db['roles']
db_transactions = db['transactions']
db_movements = db['movements']
db_rooms = db['rooms']
db_products = db['products']
db_suppliers = db['suppliers']


