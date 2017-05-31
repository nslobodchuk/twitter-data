from pymongo import MongoClient
from datetime import datetime
print("Started at", datetime.now())

client = MongoClient()
db = client.twitter_data
users = db.users

users_who_tweeted = users.find({"n_tweets": {"$gt": 0}})
users_who_were_mentioned = users.find({"n_mentions": {"$gt": 0}})
users_who_tweeted_and_were_mentioned = users.find({"n_tweets": {"$gt": 0}, "n_mentions": {"$gt": 0}})

with open("output_users_query.txt", "w+") as output:
    output.write("The number of distinct users who tweeted or were mentioned in a tweet is "
                 + str(users.count()) + "\n")
    output.write("The number of distinct users who tweeted is " + str(users_who_tweeted.count()) + "\n")
    print("Queried the number of distinct users who tweeted at", datetime.now())
    output.write("The number of distinct users who were mentioned in tweets is "
                 + str(users_who_were_mentioned.count()) + "\n")
    print("Queried the number of distinct users who were mentioned in tweets at", datetime.now())
    output.write("The number of distinct users who were mentioned in tweets and also tweeted is "
                 + str(users_who_tweeted_and_were_mentioned.count()) + "\n")
    print("Queried the number of distinct users who were mentioned in tweets and also tweeted at", datetime.now())