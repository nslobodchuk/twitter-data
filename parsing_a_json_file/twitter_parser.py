import json
import csv

print("Calculating reply relations...")

network = {}  # This is a dictionary where all reply relations between users will be stored.


def insert_user(id_str, screen_name=None):  # A function which ...
    if id_str not in network:  # ... inserts a user into the dictionary if he/she doesn't exist or ...
        network[id_str] = {"screen_name": screen_name,  # The screen name of the user
                           "n_tweets": 0,
                           "n_replies_from": 0,  # The number of times other users replied to this user
                           "n_replies_to": 0,  # The number of times this user replied to other users
                           "replies_from": {},  # The dictionary of users who replied to this user
                           "replies_to": {}  # The dictionary of users who this user replied to
                           }
    else:  # ... increments the number of tweets by the user if the user already exists.
        network[id_str]["n_tweets"] += 1

with open("tweets.json") as json_file, \
        open("errors.csv", "w+") as errors_file:  # Open the original JSON file and open an errors file for writing down errors
    errors_writer = csv.writer(errors_file)
    errors_writer.writerow(["line_number", "original_string", "error"])  # Write the headers into errors.csv file
    count = 1  # This variable will be used to track progress
    for line in json_file:
        count += 1
        try:
            line = line.strip()
            d = json.loads(line)  # Parse the line and store the reference to it in variable d.
        except:  # If an error happened while parsing the line ...
            errors_writer.writerow([str(count), line, "Error parsing the line"])  # ... write it down to errors.csv.
        else:
            if "id_str" not in d:  # If d doesn't have id_str field, it is not a valid tweet object. So ...
                errors_writer.writerow([str(count), line, "Not a tweet"])  #... write it to the errors.csv file.
            else: #  If there are no errors, ...
                insert_user(d["user"]["id_str"], d["user"]["screen_name"]) # ... pass "id_str" to insert_user function.
                if d["in_reply_to_user_id_str"] is not None:  # If the tweet is a reply ...
                    insert_user(d["in_reply_to_user_id_str"]) # ... pass  "in_reply_to_user_id_str" to insert_user function.
                    if d["in_reply_to_user_id_str"] not in network[d["user"]["id_str"]]["replies_to"]:
                        #  If the user has not replied to "in_reply_to_user_id_str", create a new entry.
                        network[d["user"]["id_str"]]["replies_to"][d["in_reply_to_user_id_str"]] = 1
                    else:
                        # If the user has already replied to "in_reply_to_user_id_str" increment the replies count.
                        network[d["user"]["id_str"]]["replies_to"][d["in_reply_to_user_id_str"]] += 1
                    # Increment the total number of times the user has replied
                    network[d["user"]["id_str"]]["n_replies_to"] += 1
                    #  If "in_reply_to_user_id_str" has not received replies from the user, create a new entry, ...
                    if d["user"]["id_str"] not in network[d["in_reply_to_user_id_str"]]["replies_from"]:
                        network[d["in_reply_to_user_id_str"]]["replies_from"][d["user"]["id_str"]] = 1
                    else:
                        # ... else increment the count
                        network[d["in_reply_to_user_id_str"]]["replies_from"][d["user"]["id_str"]] += 1
                    # Increment the total number of times "in_reply_to_user_id_str" has ...
                    # ... received replies from other users
                    network[d["in_reply_to_user_id_str"]]["n_replies_from"] += 1

        if count % 100000 == 0:  # Print a message every 10k lines
            print(count, "lines parsed.")
        count += 1

print()
print("Generating output...")

# network dictionary contains too many entries. We can't visualize them all.
# We need to leave only the most important users.
for user_id in list(network.keys()):
    if network[user_id]["n_replies_from"] < 9: #  Delete all users who received less than 10 replies from other users
        for key in network[user_id]["replies_from"]:
            del network[key]["replies_to"][user_id]
        for key in network[user_id]["replies_to"]:
            del network[key]["replies_from"][user_id]
        del network[user_id]

# Now create a dictionary following this structure: https://bl.ocks.org/mbostock/2675ff61ea5e063ede2b5d63c08020c7#miserables.json
graph = {"nodes": [], "links": []}
for user_id in network:
    graph["nodes"].append({"id": user_id,
                           "screen_name": network[user_id]["screen_name"],
                           "n_replies_from": network[user_id]["n_replies_from"]})
    for responder in network[user_id]["replies_from"]:
        value = network[user_id]["replies_from"][responder]
        del network[responder]["replies_to"][user_id]
        if responder in network[user_id]["replies_to"]:
            value += network[user_id]["replies_to"][responder]
            del network[responder]["replies_from"][user_id]
        graph["links"].append({"source": user_id, "target": responder, "value": value})


print()
print("Writing output to file...")

# Finally store the output in graph.json file
with open("graph.json", "w+") as graph_file:
    json.dump(graph, graph_file)

print("Done.")



