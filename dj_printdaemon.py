#!/usr/bin/python3
import os
import shutil


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


# Loop forever
print('Starting print daemon, Ctrl+C to exit')
while True:
  # Get files
  result = os.system('scp -i "' + dj_key + '" ' + dj_usr + '@' + dj_url + ':/opt/domjudge/print/* /tmp/dj_printdaemon/')
  if result == 0:
    for file in os.listdir('/tmp/dj_printdaemon'):
      result = os.system('lp "/tmp/dj_printdaemon/' + file + '"')
      if result == 0:
        # If successful, move it on the server, remove it locally
        print('Printed file "' + file + '", go pick it up!')
        result = os.system('ssh -i "' + dj_key + '" "mv \\"/opt/domjudge/print/' + file + '\\" \\"/opt/domjudge/printarchive/' + file + '\\""'
        if result == 0:
          os.remove('/tmp/dj_printdaemon/' + file)
        else:
          print('!!!')
          print('ERROR: ssh failed, result = ' + str(result) + ' for remote file /opt/domjudge/print/' + file)
          print('!!!')
      else:
        # Otherwise, move them for safekeeping and alert the user
        os.rename('/tmp/dj_printdaemon/' + file, '/tmp/dj_printdaemon_failure/' + file)
        print('!!!')
        print('ERROR: lp failed, result = ' + str(result) + ' for file /tmp/dj_printdaemon_failure/' + file)
        print('!!!')
  else:
    print('!!!')
    print('ERROR: scp failed, result = ' + str(result))
    print('!!!')
