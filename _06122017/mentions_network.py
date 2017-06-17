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

output_file = open("output_mention_network.csv", "w+", 1)
output_writer = csv.writer(output_file)
output_writer.writerow(["from_this_date",
                        "up_to_this_date",
                        "n_nodes",
                        "n_edges",
                        "effective_diameter_directed",
                        "effective_diameter_undirected",
                        "fraction_weakly_connected"])
while date < datetime.datetime(2016, 5, 23):
    date += datetime.timedelta(days=3)
    print datetime.datetime.now()
    print "Current end date is " + str(date)
    cursor_tweets = tweets.find({"created_at": {"$gt": date - datetime.timedelta(days=3, seconds=1), "$lt": date}})

    for d in cursor_tweets:
        insert_user(d["user"]["id_str"])

        for mentioned_user in d["entities"]["user_mentions"]:
            insert_user(mentioned_user["id_str"])
            g.AddEdge(user_dictionary[mentioned_user["id_str"]], user_dictionary[d["user"]["id_str"]])

    n_nodes = g.GetNodes()
    print n_nodes
    n_edges = g.GetEdges()
    print n_edges

    EffDiamD = snap.GetBfsEffDiam(g, 1000, True)
    print EffDiamD
    EffDiamU = snap.GetBfsEffDiam(g, 1000, False)
    print EffDiamU

    fraction = snap.GetMxWccSz(g)
    print fraction
    print "======================="

    output_writer.writerow([str(datetime.datetime(2016, 2, 7)),
                            str(date),
                            str(n_nodes),
                            str(n_edges),
                            str(EffDiamD),
                            str(EffDiamU),
                           str(fraction)])


output_file.close()
