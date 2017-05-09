from datetime import datetime
import json
import os
import zipfile
from parser import parse

start_time = datetime.now()
config_file = open("config.json")
config = json.load(config_file)
zip_files_names = os.listdir(config["path_to_zip_files"])
for zip_file_name in zip_files_names:
    zip_file = zipfile.ZipFile(os.path.join(config["path_to_zip_files"], zip_file_name))
    print("Opened", zip_file_name, datetime.now())
    files_names = zip_file.namelist()
    print("Extracting", zip_file_name, "to", config["path_to_zip_files"], datetime.now())
    zip_file.extractall(config["working_directory"])
    print("Finished extracting", zip_file_name, "to", config["path_to_zip_files"], datetime.now())
    zip_file.close()
    print("Closed", zip_file_name)
    for file_name in files_names:
        file = open(os.path.join(config["working_directory"], file_name))
        print("Opened", file_name, datetime.now())
        print("Parsing", file_name, "line by line", datetime.now())
        count = 0
        for line in file:
            parse(line, count, file_name)
            if count % 10000 == 0:
                print(str(count) + 'th line of ' + file_name)
                print(datetime.now() - start_time)
                print('\n')
            count += 1
        print("Finished parsing ", file_name, datetime.now())
        file.close()
        print("Closed", file_name, datetime.now())
        print(count, datetime.now())
        os.remove(os.path.join(config["working_directory"], file_name))
        print("Removed", file_name, datetime.now())
config_file.close()
