from pymongo import MongoClient
client = MongoClient()
db = client.twitter_data
reply_network = db.reply_network

def insert_reply_network(d):
    for key in d:
        d[key]["_id"] = key
        parent = reply_network.findOne({"_id": d[key]["parent"]})
        if parent is not None:
            parent["children"].append(key)
            parent["n_children"] += 1
            reply_network.update(
                {"_id": d[key]["parent"]},
                {
                    "$set": {
                        "children": parent["children"],
                        "n_children": parent["n_children"]
                    }
                }
            )
        else:
            reply_network.insert_one(
                {
                    "_id": d[key]["parent"],
                    "parent": None,
                    "children": [key],
                    "n_children": 1
                }
            )

        network = reply_network.findOne({"_id": key})
        if network is not None:  # duplicate tweet encountered
            if d[key]["parent"] is not None:
                network["parent"] = d[key]["parent"]
            for child in d[key]["children"]:
                if child not in network["children"]:
                    network["children"].append(child)
                    network["n_children"] += 1
            reply_network.update(
                {"_id": key},
                network
            )
        else:
            reply_network.insert_one(d[key])

            #check that all children are in database







