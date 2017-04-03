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
print('Files that fail to print will be in /tmp/dj_printdaemon_failure/')


# Create the directories, emptying the normal one first
shutil.rmtree('/tmp/dj_printdaemon')
os.makedirs('/tmp/dj_printdaemon', exist_ok=True)
os.makedirs('/tmp/dj_printdaemon_failure', exist_ok=True)


hostname = dj_usr + '@' + dj_url

remote_receive_path = Path('/opt/domjudge/print')
local_receive_path = Path('/tmp/dj_printdaemon')

remote_archive_path = Path('/opt/domjudge/printarchive')
local_archive_path = Path('/tmp/dj_printdaemon_failure')

def get_files():
    while True:
        args = [
            'scp', '-i', dj_key,
            hostname + ':' + str(remote_receive_path) + '/*',
            str(local_receive_path)
        ]
        ret = subprocess.call(args, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

        if ret != 0:
            time.sleep(5)
            continue

        yield from local_receive_path.iterdir()

# Loop forever
print('Starting print daemon, Ctrl+C to exit')
for new_file in get_files():
    subprocess.check_call(['lp', str(new_file)], stdout=subprocess.DEVNULL)
    print(datetime.datetime.today().time())
    new_file.unlink()
    subprocess.check_call([
        'ssh', '-i', dj_key, hostname,
        'mv "{}" "{}"'.format(remote_receive_path / new_file.name, remote_archive_path / new_file.name)
    ])
