import json
import sys
from pymongo import MongoClient
client = MongoClient()
db = client.twitter_data
errors = db.errors


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
        return None
    else:
        return d
