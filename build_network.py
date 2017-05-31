from datetime import datetime
from pymongo import MongoClient


startTime = datetime.now()
print("Started at", startTime)
client = MongoClient()
db = client.twitter_data
nodes = db.nodes
cursor_nodes = db.nodes.find()
networks = db.networks
if networks.count() > 0:
    print("Dropping networks", networks.count())
    networks.drop()


def network_size(_id):
    node = nodes.find({"_id": _id}).limit(1)[0]
    if node["children"] is not None:
        n_descendants = len(node["children"])
        for child in node["children"]:
            n_descendants += network_size(child)
    else:
        n_descendants = 0
    return n_descendants

count = 0
for node in cursor_nodes:
    count += 1
    if count % 1000000 == 0:
        print(str(count) + ' out of ' + str(nodes.count()) + ' done.')
        print("The number of networks is", networks.count())
        print("Now it's", datetime.now())
    if node["parent"] is not None:
        continue
    size = network_size(node["_id"])
    network = {"_id": node["_id"],
               "n_descendants": size
               }
    networks.insert_one(network)
