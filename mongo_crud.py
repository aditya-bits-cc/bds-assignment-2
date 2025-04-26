import os
from pymongo import MongoClient
from dotenv import load_dotenv

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
db = client['lung_cancer']
collection = db['lung_cancer']

# --------------------
# C - CREATE Operation
# --------------------
new_patient = [
    {"GENDER": "F", "AGE": 60, "SMOKING": 1, "YELLOW_FINGERS": 0, "ANXIETY": 1, "PEER_PRESSURE": 2, "CHRONIC_DISEASE": 1, "FATIGUE": 1, "ALLERGY": 1, 
     "WHEEZING": 1, "ALCOHOL_CONSUMING": 1, "COUGHING": 1, "SHORTNESS_OF_BREATH": 1, "SWALLOWING_DIFFICULTY": 0, "CHEST_PAIN": 1, "LUNG_CANCER": "YES"},
    {"GENDER": "M", "AGE": 60, "SMOKING": 2, "YELLOW_FINGERS": 1, "ANXIETY": 1, "PEER_PRESSURE": 1, "CHRONIC_DISEASE": 2, "FATIGUE": 1, "ALLERGY": 2,
     "WHEEZING": 1, "ALCOHOL_CONSUMING": 1, "COUGHING": 2, "SHORTNESS_OF_BREATH": 1, "SWALLOWING_DIFFICULTY": 2, "CHEST_PAIN": 2, "LUNG_CANCER": "YES"}
    ]

insert_result = collection.insert_many(new_patient)
print(f"Inserted document: {insert_result}")

# -----------------
# R - READ Operation
# -----------------
print("\nReading the db to find the Patients Diagnosed with Lung Cancer with few parameters:")
for doc in collection.find({ "LUNG_CANCER": "YES" }, { "_id": 0, "GENDER": 1, "AGE": 1, "ANXIETY": 1, "PEER_PRESSURE": 1 }):
    print(doc)

# --------------------
# U - UPDATE Operation
# --------------------
print("\nUpdating F 60 with ANXIETY to 0 and PEER_PRESSURE TO 1:")
update_result = collection.update_one(
    { "AGE": 60, "GENDER": "F" },
    { "$set": { "ANXIETY": 0, "PEER_PRESSURE": 1 } }
)
print(f"\nUpdated {update_result.modified_count} document(s)")
for doc in collection.find({ "LUNG_CANCER": "YES" }, { "_id": 0, "GENDER": 1, "AGE": 1, "ANXIETY": 1, "PEER_PRESSURE": 1 }):
    print(doc)

# --------------------
# D - DELETE Operation
# --------------------
print("\n Delete the record of Age 60 and Gender F")
delete_result = collection.delete_one({ "AGE": 60, "GENDER": "F" })
print(f"Deleted {delete_result.deleted_count} document(s), remaining records in collection:")
for document in collection.find():  # Finds all documents in the collection
    print(document)
