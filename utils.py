## LOGGING ##

import sys

def log(msg):
    if (msg[0] == '.'):
        print("INFO: " + msg[1:])
    elif (msg[0] == '#'):
        print("WARN: " + msg[1:])
    elif (msg[0] == '!'):
        print("ERROR: " + msg[1:])
        sys.exit()
    else:
        print(msg)

## VERSION HANDLING ##

from zipfile import ZipFile
import json

class Version:
    def __init__(self, version_id, is_stable, target):
        self.id = version_id
        self.is_stable = is_stable
        self.target = target

def get_version(jar_file):
    with ZipFile(jar_file) as server_jar:
        try:
            server_jar.extract('version.json')

            with open('version.json') as version_file:
                version_json = json.loads(version_file.read())

                return Version(version_json["id"], version_json["stable"], version_json["release_target"])
        except:
            log("!Could not extract version data")

    