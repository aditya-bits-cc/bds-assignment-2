# BDS Assignment 2 - MongoDB CRUD & Consistency Check

This repository is part of a Big Data Systems assignment and demonstrates:
- Executing queries using mongo shell for analysis of `dataset.json`
- Basic **CRUD operations** using MongoDB.
- Evaluation of **MongoDB consistency models** using different read and write concerns.

I tested and executed this using https://www.mongodb.com/cloud/atlas/register
Create the account, create a cluster using free tier, download the mongoshell 
Most instructions are present during setup including how to load the JSON as a collection of MongoDB

## 📁 Repository Contents

| File | Description |
|------|-------------|
| `mongo_crud.py` | Performs Create, Read, Update, and Delete operations on a MongoDB database using sample patient records. |
| `mongo_consistency_check.py` | Simulates large dataset operations to evaluate MongoDB’s read and write consistency levels. |
| `requirements.txt` | Lists required Python packages. |
| `dataset.json` | Dataset with lung cancer details |

## 👨‍🎓 Smoking & Gender-Based Analysis using MongoDB queries

1. **Total Number of Lung Cancer Diagnosed Cases**
```js
db.lung_cancer_db.aggregate([
  { $match: { LUNG_CANCER: "YES" } },
  { $group: { _id: "Total Diagnosed Cases", count: { $sum: 1 } } }
])
```

2. **Smokers with Lung Cancer**
```js
db.lung_cancer_db.aggregate([
  { $match: { SMOKING: 1, LUNG_CANCER: "YES" } },
  { $group: { _id: "Smokers with Lung Cancer", count: { $sum: 1 } } }
])
```

3. **Gender-wise Smoking and Lung Cancer Correlation**
```js
db.lung_cancer_db.aggregate([
  { $match: { SMOKING: 1, LUNG_CANCER: "YES" } },
  { $group: { _id: "$GENDER", count: { $sum: 1 } } },
  { $project: { gender: "$_id", count: 1, _id: 0 } }
])
```

4. **Average Age of Diagnosed Patients**
```js
db.lung_cancer_db.aggregate([
  { $match: { LUNG_CANCER: "YES" } },
  { $group: { _id: null, average_age: { $avg: "$AGE" } } },
  { $project: { _id: 0, description: "Average Age of Diagnosed Patients", average_age: 1 } }
])
```

5. **Number of people who smoke and have lung cancer with age and gender based distribution**
```js
db.lung_cancer_db.aggregate([
  {$match: { SMOKING: 1, LUNG_CANCER: "YES"}},
  {$facet: 
    { 
      "age_40_or_less_M": [{$match: {AGE: {$lte: 40}, GENDER: "M"}}, 
                             {$count: "count" }],
      "age_40_or_less_F": [{$match: {AGE: {$lte: 40}, GENDER: "F"}}, 
                             {$count: "count" }],
      "age_41_or_greater_M": [{ $match: {AGE: {$gt: 40}, GENDER: "M"}}, 
                              {$count: "count"}],
      "age_41_or_greater_F": [{ $match: {AGE: {$gte: 40}, GENDER: "F"}}, 
                              {$count: "count"}],
    }
  }
])
```

## 📦 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/aditya-bits-cc/bds-assignment-2.git
cd bds-assignment-2
```

### 2. Install Dependiency
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create .env file
```bash
MONGO_USERNAME=your_username
MONGO_PASSWORD=your_password
MONGO_CLUSTER=your_cluster_url
```

### 4. Run the scripts for CRUD operations
```bash
python mongo_crud.py
```

### 5. Run the scripts for read/write consistency operations
```bash
python mongo_consistency_check.py
```