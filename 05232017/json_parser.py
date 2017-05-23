import json
import csv
from accessors import accessors

with open("tweets.03.02.2016.json") as json_file, \
        open("output.csv", "w+") as output_file, \
        open("errors.csv", "w+") as errors_file:
    output_writer = csv.writer(output_file)
    errors_writer = csv.writer(errors_file)
    keys = []
    for key in accessors:
        keys.append(str(key))
    output_writer.writerow(keys)
    errors_writer.writerow(["line_number", "original_string", "error"])
    count = -1
    for line in json_file:
        count += 1
        try:
            line = line.strip()
            d = json.loads(line)
        except:
            errors_writer.writerow([str(count), line, "Error parsing the line"])
        else:
            if "id_str" not in d:
                errors_writer.writerow([str(count), line, "Not a tweet"])
            else:
                output = []
                for key in keys:
                    output.append(str(accessors[key](d)))
                output_writer.writerow(output)
