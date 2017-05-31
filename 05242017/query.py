from pymongo import MongoClient
from datetime import datetime

client = MongoClient()
db = client.twitter_data
tweets = db.tweets
handles = db.handles

n_tweets = tweets.count()
cursor_tweets = tweets.find()
# query1 = tweets.find({"entities.user_mentions.0": {"$exists": True}})
# print(query1.count())

count = -1
tweets_with_mentions_count = 0
in_reply_to_count = 0
retweets_count = 0
coordinates_count = 0
place_count = 0
coordinates_count_all = 0
place_count_all = 0
handles_count = 0

for d in cursor_tweets:
    count += 1
    if count % 1000000 == 0:
        print(count, "done out of a total of", n_tweets)
        print(datetime.now())
    user_mentions_length = len(d["entities"]["user_mentions"])
    tweets.update_one({"_id": d["_id"]},
                      {"$set": {"entities.user_mentions_length": user_mentions_length}})
    if user_mentions_length > 0:
        tweets_with_mentions_count += 1
        for user_object in d["entities"]["user_mentions"]:
            user_object["_id"] = user_object["id_str"]
            handle = handles.find({"_id": user_object["_id"]}).limit(1)
            if handle.count() == 0:
                handles.insert_one(user_object)
                handles_count += 1
        if d["in_reply_to_status_id_str"] is not None:
            in_reply_to_count += 1
        if "retweeted_status" in d:
            retweets_count += 1
        if d["coordinates"] is not None:
            coordinates_count += 1
        if d["place"] is not None:
            place_count += 1

    if d["coordinates"] is not None:
        coordinates_count_all += 1
    if d["place"] is not None:
        place_count_all += 1

print("The number of tweets is", n_tweets)
print("The number of tweets with a 'coordinates' field is", coordinates_count_all)
print("The number of tweets with a 'place' field is", place_count_all)
print("The number of tweets with mentions is", tweets_with_mentions_count)
print("Out of tweets with mentions the number of 'reply' tweets is", in_reply_to_count)
print("Out of tweets with mentions the number of retweets is", retweets_count)
print("Out of tweets with mentions the number of tweets with 'coordinates' field is", coordinates_count)
print("Out of tweets with mentions the number of tweets with 'place' field is", place_count)
print("The number of distinct handles is", handles_count)
