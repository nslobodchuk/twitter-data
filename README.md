# twitter-data
A script for processing twitter data

To instantiate a Mongo database `mongod --dbpath <path to the folder where to instantiate a database>`

The files `main.py`, `line_parser.py`, `insert_tweet.py`, and `config.json` are responsible for parsing JSON files and
storing the data into MongoDB database. It is assumed that JSON files are stored in separate daily ZIP archives.

The files `05232017/json_parser.py` and `05232017/accessors.py` are responsible for parsing a single JSON file and
storing the data in a CSV file.

The file `05242017/query_new.py` performs a query in order to produce the following descriptive statistics:

```
The total number of tweets is 164579703
The number of tweets with mentions is 132007795
Out of tweets with mentions the number of 'reply' tweets is 17799898
Out of tweets with mentions the number of retweets is 98774262
Out of tweets with mentions the number of tweets with a 'coordinates' field is 40837
Out of tweets with mentions the number of tweets with a 'place' field is 2166427
```

The file `05242017/user_ids_new.py` stores the ids of users who were mentioned in tweets and the ids of tweets'
authors in the database. The file `05242017/query_users.py` queries the users data and produces the following output:

```
The number of distinct users who tweeted or were mentioned in a tweet is 11112837
The number of distinct users who tweeted is 10642203
The number of distinct users who were mentioned in tweets is 2505764
The number of distinct users who were mentioned in tweets and also tweeted is 2035130
```

The files `build_nodes.py` and `build_network.py` are responsible for grouping the tweets into
reply networks. The file `analyze_network.py` queries the networks data and produces the following output:

```
The number of networks is 150025094
The number of networks with 1 or more descendants is 5421968
The number of networks with 2 or more descendants is 1555795
The number of networks with 3 or more descendants is 808306
The number of networks with 4 or more descendants is 527733
The number of networks with 5 or more descendants is 386748
The number of networks with 10 or more descendants is 160645
The number of networks with 50 or more descendants is 29264
The number of networks with 100 or more descendants is 14724
The number of networks with 1000 or more descendants is 1257
```
The choice of wording is poor. Here `the number of networks` means the number of networks with 1 or more nodes.
`The number of networks with 1 or more descendants` means the number of networks with 2 nodes. And so on... Note that
the number of networks if less than the number of tweets. Note also that a tweet with 0 replies is considered
a network with 1 node.


