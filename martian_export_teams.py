#!/usr/bin/python3
import json
from pathlib import Path
import random
import re


def gen_password():
  password = ''
  for i in range(3):
    # Avoid characters often confused: i, l, I, 1, o, O, 0, s, S, 5, B, 8
    password += random.choice('abcdefghjkmnpqrtuvwxyz')
    password += random.choice('.!?')
    password += random.choice('ACDEFGHJKLMNPQRTUVWXYZ')
    password += random.choice('234679')
  return password

def clean(s):
  return re.sub(' +',' ', s.strip())


# Get the category ID
dj_categ = int(input('DOMJudge category ID: '))


# Get the file
file_path = input('File path: ')
file_contents = Path(file_path).read_text()


# Convert to teams
teams = {}
idx = 0
for line in file_contents.splitlines()[1:]:
  cells = line.split(',')
  team_name = cells[1].replace(';',',')

  if team_name not in teams:
    team = {
      'user_name': 'user-' + str(idx),
      'name': team_name,
      'members': [cells[2], cells[4]],
      'category_id': dj_categ,
      'location': ' ',
      'password': gen_password(),
      'extra': []
    }
    teams[team_name] = team
    print('Imported team ' + team_name)

  idx = idx + 1

# Output the file
with open('teams.json', 'w') as teams_file:
  json.dump({'teams': list(teams.values())}, teams_file, sort_keys=True, indent=4)


print('Done!')
