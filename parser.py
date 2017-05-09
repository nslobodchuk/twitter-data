import json
import sys
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
client = MongoClient()
db = client.twitter_data
errors = db.errors
tweets = db.tweets


def parse(line, line_number, file_name):
    try:
        d = json.loads(line.strip())
    except:
        print("Error parsing the string:", str(sys.exc_info()))
        print(line)
        print('\n')
        errors.insert_one(
            {
                'file': file_name,
                'line_number': line_number,
                'line_text': line,
                'error': 'Error parsing the string',
                'exc_info': str(sys.exc_info())
            })
    else:
        if 'id_str' not in d:
            print("The string is not a valid tweet object:", str(sys.exc_info()))
            print(line)
            print('\n')
            errors.insert_one(
                {
                    'file': file_name,
                    'line_number': line_number,
                    'line_text': line,
                    'error': 'The string is not a valid tweet object',
                    'exc_info': str(sys.exc_info())
                })
            return
        d['_id'] = d['id_str']
        try:
            tweets.insert_one(d)
        except DuplicateKeyError:
            print("This is a duplicate tweet:", str(sys.exc_info()))
            print(line)
            print('\n')
            errors.insert_one(
                {
                    'file': file_name,
                    'line_number': line_number,
                    'line_text': line,
                    'error': 'This is a duplicate tweet',
                    'exc_info': str(sys.exc_info())
                })
            return
