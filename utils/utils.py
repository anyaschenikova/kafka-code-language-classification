import json
import os


def read_jsonl(path):
    with open(path, 'r') as json_file:
        json_list = list(json_file)
        for line in json_list:
            yield json.loads(line)


def read_files_from_path(path):
    for file_name in os.listdir(path):
        for el in read_jsonl(os.path.join(path, file_name)):
            yield el
