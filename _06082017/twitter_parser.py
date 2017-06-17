import json
import csv
import os


def parse_tweets(network, path_to_file):
    print("Calculating reply relations...")

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

    with open(path_to_file) as json_file, \
            open(os.path.basename(path_to_file) + ".errors.csv", "w+") as errors_file:  # Open the original JSON file and open an errors file for writing down errors
        errors_writer = csv.writer(errors_file)
        errors_writer.writerow(["line_number", "original_string", "error"])  # Write the headers into errors.csv file
        count = 1  # This variable will be used to track progress
        for line in json_file:
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

            if count % 100000 == 0:  # Print a message every 100k lines
                print(count, "lines parsed.")
            count += 1

    print("Done with", os.path.basename(path_to_file))


