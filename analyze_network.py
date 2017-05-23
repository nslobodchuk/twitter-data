from datetime import datetime
startTime = datetime.now()

from pymongo import MongoClient
import json

client = MongoClient()
db = client.twitter_data
nodes = db.nodes

cursor = nodes.find(sort=[('n_children', -1)])
node = cursor[0]
print(datetime.now() - startTime)

output = {'nodes':[], 'links':[]}



def build_output(node):
    node["n_descendants"] = node["n_children"]
    for tweet_id in node['children']:
        output['links'].append({'source': node['_id'], 'target': tweet_id})
        node_ = nodes.find_one({'_id': tweet_id})
        if node_["n_children"] > 0:
            build_output(node_)
        else:
            node_["n_descendants"] = 0
        output['nodes'].append({'id': tweet_id,
                                'n_descendants': node_['n_descendants']})
        node["n_descendants"] += node_["n_descendants"]
        

build_output(node)

output['nodes'].append({'id': node['_id'],
                        'n_descendants': node['n_descendants']})

with open('largest_network.json', 'w+') as outfile:
    json.dump(output, outfile)
    
print(datetime.now() - startTime)
