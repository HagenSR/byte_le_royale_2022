import json


def write_json_file(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)
