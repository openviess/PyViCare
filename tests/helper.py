import os
import simplejson as json

def readJson(fileName):
    test_filename = os.path.join(os.path.dirname(__file__), fileName)
    json_file = open(test_filename, mode='rb')
    try:
        return json.load(json_file)
    finally:
        json_file.close()