#!/usr/bin/python3
import csv
import json
import random


def gen_password():
  password = ''
  for i in range(3):
    password += random.choice('abcdefghijklmnopqrstuvwxyz')
    password += random.choice('.!?')
    password += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    password += random.choice('0123456789')
  return password

existing = []
config_path = input('Config file path: ')
with open(config_path, encoding='utf-8') as config_file:
  config = json.load(config_file)
  for x in config['teams']:
    existing.append(x['name'])

# Get the affiliation IDs
dj_categ_epfl = int(input('DOMJudge EPFL category ID: '))
dj_categ_ethz = int(input('DOMJudge ETHZ category ID: '))

# Get the file
file_name = input('File: ')

# Get the rows, ignore 1st as it is header
with open(file_name) as file:
  rows = list(csv.reader(file, delimiter=','))[1:]

# Convert to teams
teams = []
for idx, cells in enumerate(rows):
  if cells[0] == "": continue
  if (cells[2] + " " + cells[3]) in existing: continue

  categ = '2' # self-registered
  eligible = cells[6] == "No" and (cells[7] == "2014 or later" or cells[8] == "1995 or later") and cells[10] == "Yes"
  if cells[4] == "EPFL":
    categ = dj_categ_epfl
  elif cells[4] == "ETHZ":
    categ = dj_categ_ethz

  team = {
    'user_name': "user-" + str(idx),
    'name': cells[2] + " " + cells[3],
    'category_id': categ,
    'password': gen_password(),
  }

  config['teams'].append(team)
  print('Imported ' + team['name'])


# Output the file
with open('teams.json', 'w') as teams_file:
  json.dump(config, teams_file, sort_keys=True)


print('Done!')
