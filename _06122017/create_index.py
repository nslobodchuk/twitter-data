from pymongo import MongoClient

client = MongoClient()
db = client.twitter_data
tweets = db.tweets

tweets.create_index("created_at")