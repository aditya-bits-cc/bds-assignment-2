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
db = client.get_database("test_db1")
collection = db.get_collection("test_db1")

# Clear collection for clean testing (Optional for huge datasets, remove for bulk operations)
collection.delete_many({})

# Simulating a large dataset insert operation
large_dataset = [{"name": f"User {i}", "age": i % 1000} for i in range(1000)]

def write_data(w_val=1):
    start_time = time.time()
    collection.with_options(write_concern=WriteConcern(w=w_val)).insert_many(large_dataset)
    end_time = time.time()
    print(f"Inserting large dataset with Write Concern {w_val}... Operation completed in {end_time - start_time:.4f} seconds.")

def read_data(read_level="local"):
    start_time = time.time()
    document = collection.with_options(read_concern=ReadConcern(level=read_level)).find_one({"name": "User 50"})
    end_time = time.time()
    print(f"Reading with Read Concern '{read_level}'... Operation completed in {end_time - start_time:.4f} seconds.")

# Insert a large dataset with Write Concern w="majority" (Slower but more consistent)
write_data(w_val="majority")
read_data(read_level="majority")
read_data(read_level="local")

db = client.get_database("test_db2")
collection = db.get_collection("test_db2")
collection.delete_many({})
# Insert a large dataset with Write Concern w=1 (Faster but less consistent)
write_data(w_val=1)
read_data(read_level="majority")
read_data(read_level="local")
