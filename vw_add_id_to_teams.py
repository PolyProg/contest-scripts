#!/usr/bin/python3
import json
import sys

# Get the config
config_path = input('Config file path: ')
with open(config_path, encoding='utf-8') as config_file:
  config = json.load(config_file)


# Validate data
if 'teams' not in config:
  sys.exit('Config must contain teams')


# Add the index to teams' extra data
index = 1
for team in config['teams']:
  if 'extra' not in team:
    team['extra'] = []
  team['extra'].append('user_id: ' + str(index))
  index += 1


# Output the file
with open(config_path, 'w') as config_file:
  json.dump(config, config_file, sort_keys=True)


print('Done!')
