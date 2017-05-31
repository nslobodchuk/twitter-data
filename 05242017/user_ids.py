from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.twitter_data
tweets = db.tweets
cursor_tweets = tweets.find()
users = db.users

count = - 1
for d in cursor_tweets:
    user_cursor = users.find({"_id": d["user"]["id_str"]}).limit(1)
    if user_cursor.count() > 0:
        users.update_one({"_id": d["user"]["id_str"]}, {"$set": {"n_tweets": user_cursor[0]["n_tweets"] + 1}})
    else:
        user_to_insert = {
            "_id": d["user"]["id_str"],
            "n_tweets": 1,
            "n_mentions": 0
        }
        users.insert_one(user_to_insert)
    if len(d["entities"]["user_mentions"]) > 0:
        for user in d["entities"]["user_mentions"]:
            user_cursor = users.find({"_id": user["id_str"]}).limit(1)
            if user_cursor.count() > 0:
                users.update_one({"_id": user["id_str"]}, {"$set": {"n_mentions": user_cursor[0]["n_mentions"] + 1}})
            else:
                user_to_insert = {
                    "_id": user["id_str"],
                    "n_tweets": 0,
                    "n_mentions": 1
                }
                users.insert_one(user_to_insert)

    count += 1
    if count % 1000000 == 0:
        print(count, "done out of a total of 164579703")
        print("Users count is", users.count())
        print("Last updated user is", user_cursor[0])
        print(datetime.now())
