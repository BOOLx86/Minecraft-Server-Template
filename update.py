from utils import log
import utils
import os

os.chdir(r'D:/.minecraft/localhosts/TemplateServer')



log("!exit")

###############################################

import os
import sys
import shutil
import time
from zipfile import ZipFile
import json
import progressbar
from urllib import request
from bs4 import BeautifulSoup

# LOGGING



# ENSURING CONSISTENT WORKING DIRECTORY

os.chdir(r'C:/Users/olepl/AppData/Roaming/.minecraft/localhosts/1.16 Snapshot')

# FINDING VERSION

log('Searching for updates...', 'info')

class Version:
    def __init__(self, id):
        self.id = id

    def format():
        pass

    def toLinkFormat(self):
        return self.id #TODO

    def exists(self):
        try:
            request.urlopen('https://www.minecraft.net/en-us/article/minecraft-' + self.toLinkFormat()).read()
            return True
        except:
            return False

def findUpdate(version):
    if sys.argv[0] == '-v':
        version = Version(sys.argv[1])
        if not version.exists():
            log('You seem to be up to date! ^^', 'info')
            sys.exit()
    else:
        if version.id[-4:-1] == 'pre':
            Version(version.id).exists()
        elif '.' in version.id:
            version_split = version.id.split('.')

        elif 'w' in version.id:
            pass
        else:
            log('Invalid version of old server jar, unsupported format?', 'error')
            sys.exit()

    return version

#if is_stable or version[-4:-1] == 'pre':
#    log('The current version is not a snapshot, which is not supported by this script. Try updating manually', 'warn')
#    sys.exit()
#
#if is_stable:
#    #version_list = version.split('.')
#    pass
#else:
#    version_list = version[:-1].split('w')
#    version = version_list[0] + 'w' + str( int(version_list[1]) + 1 ) + 'a'

# FINDING LINK TO SERVER.JAR
with ZipFile('server.jar') as server_jar:
    server_jar.extract('version.json')

with open('version.json') as version_json_file:
    version_json = json.loads(version_json_file.read())

    old_version = Version(version_json['id'])
    version = findUpdate(old_version)

changelog_link = 'https://www.minecraft.net/en-us/article/minecraft-' + version.toLinkFormat()

html = request.urlopen(changelog_link).read()
bsoup = BeautifulSoup(html, features='html.parser')

for link in bsoup('a'):
    if link.text == 'Minecraft server jar':
        link_to_jar = link.get('href')
        log('Found link to server.jar', 'info')

if not link_to_jar:
    log('Could not find any matching server.jar', 'error')
    sys.exit()

# BACKING UP WORLD
log('Backing up world...', 'status')
if os.path.isdir(r'backup/update-' + version.id):
    shutil.rmtree(r'backup/update-' + version.id)

shutil.copytree(r'world', r'backup/update-' + version.id)

# BACKING UP SERVER.JAR
old_jar = r'server.jar.backup'
new_jar = r'server.jar'

if os.path.isfile(new_jar):
    if os.path.isfile(old_jar):
        os.remove(old_jar)
    os.rename(new_jar, old_jar)

# DOWNDLOAD OF SERVER.JAR
pbar = None
def show_progress(block_num, block_size, total_size):
    global pbar

    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()
    
    downloaded = block_num * block_size

    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()

log('\nDownloading server.jar...', 'status')
request.urlretrieve(url = link_to_jar, filename = new_jar, reporthook = show_progress)

log('\nSuccesfully downloaded server.jar!\n', 'status')

log('Updated from version: ' + old_version.id, 'info')
log('To version: ' + version.id + '\n', 'info')