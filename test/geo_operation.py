from pymongo import MongoClient

# 访问lulinlin数据库
client = MongoClient("mongodb://localhost:27017/")
db = client["lulinlin"]
coll = db["lulinlin_col"]

# x = coll.find_one()
# print(x)

# 创建索引
coll.create_index([("geometry", "2dsphere")])
# 用直线（84.06，26.18）--（109.56，46.02）进行intersect查询
doc = coll.find({
    "geometry": {"$geoIntersects": {"$geometry": {"type": "LineString", "coordinates":
        [[84.06, 26.18], [109.56, 46.02]]}}}}, {"properties": 1})
print("查询结果属性信息为：{}".format(doc))
# 关闭数据库连接
client.close()
