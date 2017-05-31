from pymongo import MongoClient
from datetime import datetime
print("Started at", datetime.now())

client = MongoClient()
db = client.twitter_data
tweets = db.tweets

tweets_with_mentions = tweets.find({"entities.user_mentions.0": {"$exists": True}})
reply_tweets = tweets.find({"entities.user_mentions.0": {"$exists": True}, "in_reply_to_status_id_str": {"$ne": None}})
retweets = tweets.find({"entities.user_mentions.0": {"$exists": True}, "retweeted_status": {"$exists": True}})
tweets_with_coordinates = tweets.find({"entities.user_mentions.0": {"$exists": True}, "coordinates": {"$ne": None}})
tweets_with_place = tweets.find({"entities.user_mentions.0": {"$exists": True}, "place": {"$ne": None}})
# id_handles = tweets.distinct("entities.user_mentions.id_str", {"entities.user_mentions.0": {"$exists": True}})

with open("output.txt", "w+") as output:
    output.write("The total number of tweets is " + str(tweets.count()) + "\n")
    output.write("The number of tweets with mentions is " + str(tweets_with_mentions.count()) + "\n")
    print("Queried tweets with mentions at", datetime.now())
    output.write("Out of tweets with mentions the number of 'reply' tweets is " + str(reply_tweets.count()) + "\n")
    print("Queried reply tweets at", datetime.now())
    output.write("Out of tweets with mentions the number of retweets is " + str(retweets.count()) + "\n")
    print("Queried retweets at", datetime.now())
    output.write("Out of tweets with mentions the number of tweets with a 'coordinates' field is " +
                 str(tweets_with_coordinates.count()) + "\n")
    print("Queried tweets with coordinates at", datetime.now())
    output.write("Out of tweets with mentions the number of tweets with a 'place' field is " +
                 str(tweets_with_place.count()) + "\n")
    print("Queried tweets with place at", datetime.now())
    # output.write("The number of distinct user mentions in tweets is " +
    #              str(len(id_handles)) + "\n")
    # print("Queried distinct id handles at", datetime.now())

# with open("handles.txt", "w+") as handles_file:
#     for handle in id_handles:
#         handles_file.write(handle)
#         handles_file.write("\n")
