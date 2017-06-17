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


def insert_user(user_id_str):
    if user_id_str not in user_dictionary:
        user_dictionary[user_id_str] = index[0]
        user_array.append(user_id_str)
        g.AddNode(user_dictionary[user_id_str])
        index[0] += 1

date = datetime.datetime(2016, 2, 7)

output_file = open("output.csv", "w+", 1)
output_writer = csv.writer(output_file)
output_writer.writerow(["from_this_date",
                        "up_to_this_date",
                        "n_nodes",
                        "n_edges",
                        "effective_diameter_directed",
                        "effective_diameter_undirected"])
while date < datetime.datetime(2016, 6, 1):
    date += datetime.timedelta(days=3)
    print datetime.datetime.now()
    print "Current end date is " + str(date)
    cursor_tweets = tweets.find({"created_at":{"$gt": date - datetime.timedelta(days=3, seconds=1), "$lt": date}})

    for d in cursor_tweets:
        insert_user(d["user"]["id_str"])
        if d["in_reply_to_user_id_str"] is not None:
            insert_user(d["in_reply_to_user_id_str"])
            g.AddEdge(user_dictionary[d["in_reply_to_user_id_str"]], user_dictionary[d["user"]["id_str"]])

    EffDiamD = snap.GetBfsEffDiam(g, 1000, True)
    EffDiamU = snap.GetBfsEffDiam(g, 1000, False)

    n_nodes = g.GetNodes()
    n_edges = g.GetEdges()

    output_writer.writerow([str(datetime.datetime(2016, 2, 7)),
                            str(date),
                            str(n_nodes),
                            str(n_edges),
                            str(EffDiamD),
                            str(EffDiamU)])

    print n_nodes
    print n_edges
    print EffDiamD
    print EffDiamU

output_file.close()



