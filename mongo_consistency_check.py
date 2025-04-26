import os
import time
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern

# Load environment variables from .env file
load_dotenv()

# Read variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")

# MongoDB connection string
MONGO_URI = f"mongodb+srv://{username}:{password}@{cluster}/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Simulating a dataset insert operation
large_dataset = [{"name": f"User {i}", "age": i % 1000} for i in range(1000)]

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Operation `{func.__name__}` completed in {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@timer
def write_data(w_val=1):
    print(f"\nInserting large dataset with Write Concern {w_val}...", end=" ")
    collection.with_options(write_concern=WriteConcern(w=w_val)).insert_many(large_dataset)
    return None

@timer
def read_data(read_level="local"):
    print(f"Reading with Read Concern '{read_level}'...", end=" ")
    collection.with_options(read_concern=ReadConcern(level=read_level)).find_one({"name": "User 50"})
    return None


# DB and collection for w=majority
db = client.get_database("test_db1")
collection = db.get_collection("test_db1")
collection.delete_many({}) 

# Insert a large dataset with Write Concern w="majority" (Slower but more consistent)
write_data(w_val="majority")
read_data(read_level="majority")
read_data(read_level="local")

# Different collection for w=1
db = client.get_database("test_db2")
collection = db.get_collection("test_db2")
collection.delete_many({}) # Clear the db for testing if already populated

# Insert a large dataset with Write Concern w=1 (Faster but less consistent)
write_data(w_val=1)
read_data(read_level="majority")
read_data(read_level="local")
