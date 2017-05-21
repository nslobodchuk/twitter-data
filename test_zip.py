import json
import os
import zipfile

config = {
  "path_to_zip_files": "/Users/nslobodchuk/Projects/twitter-data/twitter-data-zip_",
  "working_directory": "/Users/nslobodchuk/Projects/twitter-data/twitter-data-working-directory"
}
zip_files_names = os.listdir(config["path_to_zip_files"])
output = "#!/bin/bash \n"
for zip_file_name in zip_files_names:
    if not zip_file_name.lower().endswith(".zip"):
        continue
    output += "unzip twitter-data-zip_/" + zip_file_name + " -d twitter-data-zip \n"
    zip_file = zipfile.ZipFile(os.path.join(config["path_to_zip_files"], zip_file_name))
    files_names = zip_file.namelist()
    output += "zip -j twitter-data-zip/" + zip_file_name +  " twitter-data-zip/"+files_names[0]+"\n"
    output += "rm twitter-data-zip/" + files_names[0] + "\n\n"
    zip_file.close()

print(output)
