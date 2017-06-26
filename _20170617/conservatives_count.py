from pymongo import MongoClient
import datetime
import snap
import csv

client = MongoClient()
db = client.twitter_data
tweets = db.tweets

g = snap.TNGraph.New()
user_dictionary = {}
user_array = []
index = [0]

words = ["conservative",
            "gop",
            "republican",
            "moderate",
            "independent",
            "liberal",
            "progressive",
            "democrat"]


def description_contains(d, word):
    if word in d["user"]["description"]:
        return True
    return False


def process_tweet(d):
    if d["user"]["id_str"] not in user_dictionary:
        user_dictionary[d["user"]["id_str"]] = {
            "n_trump_mentions": 0,
            "n_clinton_mentions": 0
        }
        if d["user"]["description"] is None:
            d["user"]["description"] = ""
        d["user"]["description"] = d["user"]["description"].lower()
        for word in words:
            user_dictionary[d["user"]["id_str"]][word] = description_contains(d, word)
    for mentioned_user in d["entities"]["user_mentions"]:
        if mentioned_user["id_str"] == "25073877":
            user_dictionary[d["user"]["id_str"]]["n_trump_mentions"] += 1
        if mentioned_user["id_str"] == "1339835893":
            user_dictionary[d["user"]["id_str"]]["n_clinton_mentions"] += 1

for d in tweets.find():
    process_tweet(d)

results = {
    "republican": {
        "n_tweets_trump": 0,
        "n_tweets_clinton": 0,
        "n_users_trump": 0,
        "n_users_clinton": 0
    },
    "moderate": {
        "n_tweets_trump": 0,
        "n_tweets_clinton": 0,
        "n_users_trump": 0,
        "n_users_clinton": 0
    },
    "democrat": {
        "n_tweets_trump": 0,
        "n_tweets_clinton": 0,
        "n_users_trump": 0,
        "n_users_clinton": 0
    },
    "uncategorized": {
        "n_tweets_trump": 0,
        "n_tweets_clinton": 0,
        "n_users_trump": 0,
        "n_users_clinton": 0
    }
}

for user_id in user_dictionary:
    if user_dictionary[user_id]["conservative"] is True or \
            user_dictionary[user_id]["gop"] is True or \
            user_dictionary[user_id]["republican"] is True:
        results["republican"]["n_tweets_trump"] += user_dictionary[user_id]["n_trump_mentions"]
        results["republican"]["n_tweets_clinton"] += user_dictionary[user_id]["n_clinton_mentions"]
        results["republican"]["n_users_trump"] += min(user_dictionary[user_id]["n_trump_mentions"], 1)
        results["republican"]["n_users_clinton"] += min(user_dictionary[user_id]["n_clinton_mentions"], 1)

    if user_dictionary[user_id]["independent"] is True or \
            user_dictionary[user_id]["moderate"] is True:
        results["moderate"]["n_tweets_trump"] += user_dictionary[user_id]["n_trump_mentions"]
        results["moderate"]["n_tweets_clinton"] += user_dictionary[user_id]["n_clinton_mentions"]
        results["moderate"]["n_users_trump"] += min(user_dictionary[user_id]["n_trump_mentions"], 1)
        results["moderate"]["n_users_clinton"] += min(user_dictionary[user_id]["n_clinton_mentions"], 1)

    if user_dictionary[user_id]["liberal"] is True or \
            user_dictionary[user_id]["progressive"] is True or \
            user_dictionary[user_id]["democrat"] is True:
        results["democrat"]["n_tweets_trump"] += user_dictionary[user_id]["n_trump_mentions"]
        results["democrat"]["n_tweets_clinton"] += user_dictionary[user_id]["n_clinton_mentions"]
        results["democrat"]["n_users_trump"] += min(user_dictionary[user_id]["n_trump_mentions"], 1)
        results["democrat"]["n_users_clinton"] += min(user_dictionary[user_id]["n_clinton_mentions"], 1)

    if user_dictionary[user_id]["conservative"] is False and \
             user_dictionary[user_id]["gop"] is False and \
             user_dictionary[user_id]["republican"] is False and\
             user_dictionary[user_id]["independent"] is False and \
             user_dictionary[user_id]["moderate"] is False and\
            user_dictionary[user_id]["liberal"] is False and\
            user_dictionary[user_id]["progressive"] is False and \
            user_dictionary[user_id]["democrat"] is False:
        results["uncategorized"]["n_tweets_trump"] += user_dictionary[user_id]["n_trump_mentions"]
        results["uncategorized"]["n_tweets_clinton"] += user_dictionary[user_id]["n_clinton_mentions"]
        results["uncategorized"]["n_users_trump"] += min(user_dictionary[user_id]["n_trump_mentions"], 1)
        results["uncategorized"]["n_users_clinton"] += min(user_dictionary[user_id]["n_clinton_mentions"], 1)


output_file = open("output.csv", "w+")
output_writer = csv.writer(output_file)
output_writer.writerow(["type",
            "n_tweets_trump",
            "n_tweets_clinton",
            "n_users_trump",
            "n_users_clinton"])
output_writer.writerow(["republican",
                        results["republican"]["n_tweets_trump"],
                        results["republican"]["n_tweets_clinton"],
                        results["republican"]["n_users_trump"],
                        results["republican"]["n_users_clinton"]
                        ])

output_writer.writerow(["moderate",
                        results["moderate"]["n_tweets_trump"],
                        results["moderate"]["n_tweets_clinton"],
                        results["moderate"]["n_users_trump"],
                        results["moderate"]["n_users_clinton"]
                        ])
output_writer.writerow(["democrat",
                        results["democrat"]["n_tweets_trump"],
                        results["democrat"]["n_tweets_clinton"],
                        results["democrat"]["n_users_trump"],
                        results["democrat"]["n_users_clinton"]
                        ])
output_writer.writerow(["uncategorized",
                        results["uncategorized"]["n_tweets_trump"],
                        results["uncategorized"]["n_tweets_clinton"],
                        results["uncategorized"]["n_users_trump"],
                        results["uncategorized"]["n_users_clinton"]
                        ])

output_file.close()
