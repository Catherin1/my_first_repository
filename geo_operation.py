from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["stzhou"]
coll = db["china"]
 
#x = coll.find_one()
#print(x)

#coll.create_index('{"geometry": "2dsphere" }')

filter = {"geometry": {"$geoIntersects": {"$geometry": {"type": "LineString","coordinates": \
     [[84.26, 27.34], [108.95, 45.22]]}} } }
projection = {"_id": 0, "properties":1}

for doc in coll.find(filter, projection):
    print(doc)
 