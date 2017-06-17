from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.twitter_data
tweets = db.tweets
cursor_tweets = tweets.find()

count = 0
for d in cursor_tweets:
    date = datetime.strptime(d["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
    tweets.update_one({"_id": d["_id"]}, {"$set":{"created_at": date}})
    count += 1
    if count % 1000000 == 0:
        print(count, date, datetime.now())
