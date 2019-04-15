#!/usr/bin/python3

import csv
import json
import os
import sys

# Get the config
config_path = input('Config file path: ')
with open(config_path, encoding='utf-8') as config_file:
  config = json.load(config_file)

# Validate data
if 'teams' not in config:
  sys.exit('Config must contain teams')
all_locs = set()
teams = config['teams']
for team in teams:
  if 'name' not in team:
    sys.exit('Teams must have name, password')
  if 'location' in team:
    if team['location'] in all_locs:
      sys.exit('Duplicate location found: ' + team['location'])
    all_locs.add(team['location'])

# Sort teams
sorted_teams = sorted(config['teams'], key=lambda t: t['name'])

os.makedirs('out', exist_ok=True)
with open('out/plan.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
  writer = csv.writer(csvfile, dialect='excel')
  for team in sorted_teams:
    # add tabs so excel treats as text
    writer.writerow([team['name'] + "\t", team['location'] + "\t"])

print('Done! Output is in out/plan.csv, meant for Excel')
