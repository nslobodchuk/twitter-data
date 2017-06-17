from pymongo import MongoClient
from datetime import datetime
print("Started at", datetime.now())

client = MongoClient()
db = client.twitter_data
tweets = db.tweets

d = tweets.find_one({"created_at": datetime.strptime("Sun Feb 07 19:18:02 +0000 2016", "%a %b %d %H:%M:%S +0000 %Y")})

print(d["created_at"])