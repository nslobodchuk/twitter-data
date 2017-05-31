import csv
from pymongo import MongoClient

client = MongoClient()
db = client.twitter_data
networks = db.networks
nodes = db.nodes

# gt0_networks = networks.find({"n_descendants": {"$gt": 0}})
# gt1_networks = networks.find({"n_descendants": {"$gt": 1}})
# gt2_networks = networks.find({"n_descendants": {"$gt": 2}})
# gt3_networks = networks.find({"n_descendants": {"$gt": 3}})
# gt4_networks = networks.find({"n_descendants": {"$gt": 4}})
# gt9_networks = networks.find({"n_descendants": {"$gt": 9}})
# gt49_networks = networks.find({"n_descendants": {"$gt": 49}})
# gt99_networks = networks.find({"n_descendants": {"$gt": 99}})
# gt999_networks = networks.find({"n_descendants": {"$gt": 999}})
#
# with open("networks_description.txt", "w+") as analysis_file:
#     analysis_file.write("The number of networks is " + str(networks.count()) + "\n")
#     analysis_file.write("The number of networks with 1 or more descendants is " + str(gt0_networks.count()) + "\n")
#     analysis_file.write("The number of networks with 2 or more descendants is " + str(gt1_networks.count()) + "\n")
#     analysis_file.write("The number of networks with 3 or more descendants is " + str(gt2_networks.count()) + "\n")
#     analysis_file.write("The number of networks with 4 or more descendants is " + str(gt3_networks.count()) + "\n")
#     analysis_file.write("The number of networks with 5 or more descendants is " + str(gt4_networks.count()) + "\n")
#     analysis_file.write("The number of networks with 10 or more descendants is " + str(gt9_networks.count()) + "\n")
#     analysis_file.write("The number of networks with 50 or more descendants is " + str(gt49_networks.count()) + "\n")
#     analysis_file.write("The number of networks with 100 or more descendants is " + str(gt99_networks.count()) + "\n")
#     analysis_file.write("The number of networks with 1000 or more descendants is " + str(gt999_networks.count()) + "\n")


def build_output(parent_id):
    node = nodes.find({"_id": parent_id}).limit(1)[0]
    if node["children"] is not None:
        for child in node["children"]:
            output_writer.writerow([network["_id"], parent_id, child])
            build_output(child)

cursor = networks.find(sort=[('n_descendants', -1)]).limit(100)

count = 1
with open("100_largest_networks.csv", "w+") as output_file:
    output_writer = csv.writer(output_file)
    output_writer.writerow(["root", "parent", "child"])
    for network in cursor:
        print(count)
        build_output(network["_id"])
        count += 1
