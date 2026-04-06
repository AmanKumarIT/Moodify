import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

# Load env variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "moodify_db")

class MongoDB:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance

    @property
    def db(self):
        if self._db is None:
            try:
                print(f"Connecting to MongoDB at {MONGO_URI}")
                self._client = MongoClient(MONGO_URI, server_api=ServerApi('1'), serverSelectionTimeoutMS=5000)
                # Test connection
                self._client.admin.command('ping')
                self._db = self._client[DB_NAME]
                
                # Ensure indexes
                self._db.users.create_index("email", unique=True)
                self._db.users.create_index("username", unique=True)
                print("MongoDB connection established and indexes verified.")
            except Exception as e:
                print(f"CRITICAL: Failed to connect to MongoDB: {e}")
                # We return None or re-raise depending on preference; 
                # here we'll let it raise so the view can catch it and return 500
                raise ConnectionError(f"Database connection failed: {e}")
        return self._db

# Export a singleton instance of the database
db_instance = MongoDB()
# We export a proxy object that will trigger the lazy connection
class DBProxy:
    def __getattr__(self, name):
        database = db_instance.db
        return getattr(database, name)

db = DBProxy()
