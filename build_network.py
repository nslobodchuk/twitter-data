from datetime import datetime
from pymongo import MongoClient

'''
network_template = {
_id: twitter Id_str,
parent: null or twitter id_str
children: null or array of id_str's [id_str1,id_str2,...]
n_children: length of children array
}
'''

startTime = datetime.now()
client = MongoClient()
db = client.twitter_data
nodes = db.nodes

cursor_tweets = db.tweets.find()

iteration = 0

for document in cursor_tweets:
    iteration += 1
    if iteration % 100000 == 0:
        print(str(iteration) + ' of ' + str(cursor_tweets.count()) + ' done.')
        print(datetime.now() - startTime)
    cursor = nodes.find({'_id': document['_id']}).limit(1)
    if cursor.count() == 0:
        node = {
            '_id': document['_id'],
            'children': None,
            'parent': None,
            'n_children': 0
        }
        nodes.insert_one(node)
    if 'in_reply_to_status_id_str' in document and \
                    document['in_reply_to_status_id_str'] is not None:
        nodes.update_one(
            {'_id': document['_id']},
            {'$set': {'parent': document['in_reply_to_status_id_str']}}
        )
        cursor = nodes.find({'_id': document['in_reply_to_status_id_str']}).limit(1)
        if cursor.count() == 0:
            parent_node = {
                    '_id': document['in_reply_to_status_id_str'],
                    'children': [document['_id']],
                    'parent': None,
                    'n_children': 1
                    }
            nodes.insert_one(parent_node)
        else:
            parent_node = cursor[0]
            if parent_node['children'] is None:
                nodes.update_one(
                    {'_id': document['in_reply_to_status_id_str']},
                    {'$set': {'children': [document['_id']],
                              'n_children': 1}
                     })
            else:
                parent_node['children'].append(document['_id'])
                parent_node['n_children'] += 1
                nodes.update_one(
                    {'_id': document['in_reply_to_status_id_str']},
                    {'$set': {'children': parent_node['children'],
                              'n_children': parent_node['n_children']}
                     })

print(datetime.now() - startTime)
