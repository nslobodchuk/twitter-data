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
        g.AddNode(index[0])
        index[0] += 1


output_file = open("node_centrality.csv", "w+", 1)
output_writer = csv.writer(output_file)
output_writer.writerow(["node",
                        "centrality"])

cursor_tweets = tweets.find({"created_at": {"$gt": datetime.datetime(2016, 2, 14), "$lt": datetime.datetime(2016, 2, 15)}})

for d in cursor_tweets:
    insert_user(d["user"]["id_str"])

    for mentioned_user in d["entities"]["user_mentions"]:
        insert_user(mentioned_user["id_str"])
        g.AddEdge(user_dictionary[mentioned_user["id_str"]], user_dictionary[d["user"]["id_str"]])
print "Finished building network. Calculating betweenness centrality now."
n_nodes = g.GetNodes()
print "Number of nodes: " + str(n_nodes)
n_edges = g.GetEdges()
print "Number of edges: " + str(n_edges)

Nodes = snap.TIntFltH()
Edges = snap.TIntPrFltH()
snap.GetBetweennessCentr(g, Nodes, Edges, 0.2, True)

for node in Nodes:
    output_writer.writerow([user_array[node], Nodes[node]])

output_file.close()

ids = []
with open("ids_with_names.txt") as ids_file, open("ids_with_names_centrality.csv", "w+") as output_file_2:
    ids_reader = csv.reader(ids_file, delimiter="\t")
    output_writer_2 = csv.writer(output_file_2)
    output_writer_2.writerow(["district", "member", "handle", "type", "party", "twitter_id", "centrality"])
    for row in ids_reader:
        id_str = str(row[5])
        if id_str in user_dictionary:
            centrality = Nodes[user_dictionary[id_str]]
            row.append(centrality)
            output_writer_2.writerow(row)
