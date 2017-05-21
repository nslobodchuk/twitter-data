from datetime import datetime
import json
import os
import zipfile
from line_parser import parse
from insert_tweet import insert_tweet

start_time = datetime.now()
config_file = open("/Users/nslobodchuk/Projects/twitter-data/twitter-data-code/config.json")
config = json.load(config_file)
config_file.close()
zip_files_names = os.listdir(config["path_to_zip_files"])
for zip_file_name in zip_files_names:
    if not zip_file_name.lower().endswith(".zip"):
        continue
    zip_file = zipfile.ZipFile(os.path.join(config["path_to_zip_files"], zip_file_name))
    print("Opened", zip_file_name, datetime.now() - start_time)
    files_names = zip_file.namelist()
    print("Extracting", zip_file_name, "to", config["path_to_zip_files"], datetime.now() - start_time)
    zip_file.extractall(config["working_directory"])
    print("Finished extracting", zip_file_name, "to", config["path_to_zip_files"], datetime.now() - start_time)
    zip_file.close()
    print("Closed", zip_file_name)
    for file_name in files_names:
        file = open(os.path.join(config["working_directory"], file_name))
        print("Opened", file_name, datetime.now() - start_time)
        print("Parsing", file_name, "line by line", datetime.now() - start_time)
        count = 0
        for line in file:
            d = parse(line, count, file_name)
            if d is not None:
                insert_tweet(d, line, count, file_name)
            if count % 100000 == 0:
                print(str(count) + 'th line of ' + file_name)
                print(datetime.now() - start_time)
                print('\n')
            count += 1
        print("Finished parsing ", file_name, datetime.now() - start_time)
        file.close()
        print("Closed", file_name, datetime.now() - start_time)
        print(count, datetime.now() - start_time)
        os.remove(os.path.join(config["working_directory"], file_name))
        print("Removed", file_name, datetime.now() - start_time)
