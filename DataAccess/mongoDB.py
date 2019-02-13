import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
test = db.test
res = test.insert_one({'name':"李白", "age":"30", "skill":"Python"})
print(res)
print(res.inserted_id)

data = test.find_one({'_id':ObjectId(res.inserted_id)})

print(data)

