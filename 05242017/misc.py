from pymongo import MongoClient

client = MongoClient()
db = client.twitter_data
tweets = db.tweets
cursor = tweets.find()

with open("misc_output.txt", "w+") as output:
    count = -1
    for d in cursor:
        if len(d["entities"]["user_mentions"]) > 0:
            output.write("id_str: " + d["id_str"]+ "\n")
            output.write("text: " + d["text"] + "\n")
            output.write("entities.user_mentions: " + str(d["entities"]["user_mentions"]) + "\n\n")
            count += 1
            if count > 999:
                break
