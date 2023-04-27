from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["lulinlin"]
coll = db["lulinlin_col"]
 
# x = coll.find_one()
# print(x)

coll.create_index([("geometry", "2dsphere")])

# coll.create_index([("geometry", "2dsphere")])


filter = {"geometry": {"$geoIntersects": {"$geometry": {"type": "LineString","coordinates":
     [[84.06,26.18], [109.56,46.02]]}} } }
projection = {"properties":1}

# for doc in coll.find(filter, projection):
#     print(doc)

client.close()