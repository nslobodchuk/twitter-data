from insert_reply_network import insert_reply_network

class Build_Network():
    def __init__(self):
        self.reply_network = {}
        self.n_tweets = 100000

    def process_line(self, d):
        self.reply_network[d["id_str"]] = {
            "root": d["id_str"],
            "parent": d["in_reply_to_status_id"],
            "children":[],
            "n_children": 0
        }

        if d["in_reply_to_status_id"]!= None and d["in_reply_to_status_id"] in self.reply_network:
            self.reply_network[d["in_reply_to_status_id"]]["children"].append(d["id_str"])
            self.reply_network[d["in_reply_to_status_id"]]["n_children"] += 1


        self.n_tweets += 1
        self.store_in_database()

    def store_in_database(self):
        if self.n_tweets >= 100000:
            insert_reply_network(self.reply_network)
            self.reply_network = {}
            self.n_tweets = 0









