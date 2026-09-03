from pymongo import MongoClient

MONGO_URL = "mongodb+srv://07gaganasomashekar_db_user:max1015@cluster0.d4g8ltr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URL)

db = client["pharmacy_ai"]

pharmacies_collection = db["pharmacies"]
users_collection = db["users"]
medicines_collection = db["medicines"]
bills_collection = db["bills"]