#!/usr/bin/python3
import json
import os
import sys
import time

# Get the config
config_path = input('Config file path: ')
with open(config_path, encoding='utf-8') as config_file:
  config = json.load(config_file)


# Validate data
if 'teams' not in config:
  sys.exit('Config must contain teams')
teams = config['teams']
for team in teams:
  if 'user_name' not in team or 'password' not in team:
    sys.exit('Teams must have user_name, password')


# Import teams
domain = 'OU=POLYPROG-Workstations,OU=POLYPROG,OU=SCIENC-CULT,OU=ASSOCIATIONS,OU=EHE,DC=intranet,DC=epfl,DC=ch'
uid = 500000
gid = 11172 # should probably (?) be the GID of the user configured to use adtool

for team in teams:
  os.system('adtool usercreate ' + team['user_name'] + ' ' + domain)

# make sure changes have propagated
#time.sleep(10)

for idx, team in enumerate(teams):
  os.system('adtool setpass ' + team['user_name'] + " '" + team['password'] + "'")
  os.system('adtool userunlock ' + team['user_name'])
  os.system('adtool attributereplace ' + team['user_name'] + ' uid ' + team['user_name'])
  os.system('adtool attributereplace ' + team['user_name'] + ' uidNumber ' + str(uid + idx))
  os.system('adtool attributereplace ' + team['user_name'] + ' gidNumber ' + str(gid))

print('Done!')
