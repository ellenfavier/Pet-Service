from pymongo import MongoClient
from app.settings import settings

# Используем 'settings' вместо 'os.getenv'
client = MongoClient(settings.MONGO_URI)
db = client[settings.DB_NAME]