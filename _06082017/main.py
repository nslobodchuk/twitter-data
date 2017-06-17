from datetime import datetime
import os
import zipfile
from twitter_parser import parse_tweets

network = {}
zip_directory = "/Users/nslobodchuk/Projects/twitter-data/twitter-data-zip"
working_directory = "/Users/nslobodchuk/Projects/twitter-data/twitter-data-working-directory"
zip_file_names = os.listdir(zip_directory)
zip_file_names.sort()
for zip_file_name in zip_file_names:
    if not zip_file_name.lower().endswith(".zip"):
        continue
    with zipfile.ZipFile(os.path.join(zip_directory, zip_file_name)) as zip_file:
        file_names = zip_file.namelist()
        zip_file.extractall(working_directory)
        print("Extracted", zip_file_name, "to", working_directory, datetime.now())
        for file_name in file_names:
            if not file_name.lower().endswith(".json"):
                continue
            else:
                parse_tweets(network, os.path.join(working_directory, file_name))
            os.remove(os.path.join(working_directory, file_name))
            keys_list = list(network.keys())
            print(len(keys_list))
            print("Removed", file_name, "from", working_directory, datetime.now())


