from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.twitter_data
tweets = db.tweets
cursor_tweets = tweets.find()

users_dict = {}

count = -1
for d in cursor_tweets:
    if d["user"]["id_str"] not in users_dict:
        users_dict[d["user"]["id_str"]] = {
            "_id": d["user"]["id_str"],
            "n_tweets": 1,
            "n_mentions": 0
        }
    else:
        users_dict[d["user"]["id_str"]]["n_tweets"] += 1
    for mentioned_user in d["entities"]["user_mentions"]:
        if mentioned_user["id_str"] not in users_dict:
            users_dict[mentioned_user["id_str"]] = {
                "_id": mentioned_user["id_str"],
                "n_tweets": 0,
                "n_mentions": 1
            }
        else:
            users_dict[mentioned_user["id_str"]]["n_mentions"] += 1
    count += 1
    if count % 1000000 == 0:
        print(count, "done out of a total of 164579703")
        print(datetime.now())
        print("size of dictionary is", len(users_dict))

users = db.users
count = -1
for key in users_dict:
    users.insert_one(users_dict[key])
    count += 1
    if count % 1000000 == 0:
        print(count, "inserted")
        print("Size of users is", users.count())
        print(datetime.now())

