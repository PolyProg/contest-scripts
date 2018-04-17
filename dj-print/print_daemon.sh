#!/usr/bin/env python3
import datetime
import os
import shutil
import subprocess
import time
from pathlib import Path

# Get the DOMJudge host and SSH private key
dj_url = input('DOMJudge host: ')
dj_usr = input('Username for DOMJudge host: ')
dj_key = input('Path to SSH private key for DOMJudge host: ')


print('This script assumes that the documents to be printed are in /opt/domjudge/print/ on the remote server')
print('Once printed, they will be moved to /opt/domjudge/printarchive/ on the remote server')



hostname = dj_usr + '@' + dj_url

remote_receive_path = Path('/opt/domjudge/print')
local_receive_path = Path('/mnt/d/HC2PRINT')
remote_archive_path = Path('/opt/domjudge/printarchive')

# Create the directories, emptying the normal one first
#shutil.rmtree('/mnt/d/HC2PRINT')
os.makedirs('/mnt/d/HC2PRINT', exist_ok=True)

def get_files():
    while True:
        args = [
            'ssh', '-i', dj_key,
            hostname,
            "bash -c 'sudo docker cp server:/opt/domjudge/print .'"
        ]
        ret = subprocess.call(args) #, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        if ret != 0:
            time.sleep(5)
            continue

        line='scp -r -i ' + dj_key + ' ' + hostname + ':print/* /mnt/d/HC2PRINT/ > /dev/null 2>&1'
        #print(line)
        os.system(line)
        #ret = subprocess.call(args) #, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        args = [
            'ssh', '-i', dj_key,
            hostname,
            "bash -c 'rm -rf print'"
        ]
        ret = subprocess.call(args) #, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        if ret != 0:
            time.sleep(5)
            continue

        yield from local_receive_path.iterdir()

# Loop forever
print('Starting print daemon, Ctrl+C to exit')
for new_file in get_files():
    subprocess.call(['ps2pdf', '/mnt/d/HC2PRINT/' + new_file.name, '/mnt/d/HC2PRINTPDF/' + new_file.name + '.pdf'])
    subprocess.call(['rm', '/mnt/d/HC2PRINT/' + new_file.name])
    print("")
    print("!!!!!!")
    print(datetime.datetime.today().time())
    #new_file.unlink()
    subprocess.call([
        'ssh', '-i', dj_key, hostname,
        'sudo docker exec server bash -c ' + "'" + 'mv ' + str(remote_receive_path / new_file.name).replace('.pdf','') + ' ' + str(remote_archive_path / new_file.name) + "'"
    ])
