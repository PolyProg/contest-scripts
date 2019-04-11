#!/usr/bin/python3
from bs4 import BeautifulSoup
import json
import random
import re
import requests

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


# Make up the list of locations
# We have 3 rooms: CO 020, CO 021, CO 023
# CO 020 and 023 have the same layout: 5 rows of 9 computers, which are too close to each other so we use 4 per row
# CO 021 has 10 rows of 6 computers, far apart to have one team per computer
# We additionally reserve 2 rows of CO 023 for emergency needs, e.g. a computer fails and a team needs to be moved
locations = []
for c in range(0,  5):
  for r in range(4):
    locations.append('20-' + str(c).zfill(2) + '-' + str(1 + r * 2).zfill(2))
for c in range(0, 10):
  for r in range(6):
    locations.append('21-' + str(c).zfill(2) + '-' + str(r).zfill(2))
for c in range(2,  5):
  for r in range(4):
    locations.append('23-' + str(c).zfill(2) + '-' + str(1 + r * 2).zfill(2))

# Get the category IDs
dj_categ_student = int(input('DOMJudge students category ID: '))
dj_categ_pro = int(input('DOMJudge professionals category ID: '))


# Get the session cookie
hc2_secret = input('HC2.ch secret: ')


# Get the teams list
hc2_req = requests.get('http://my.hc2.ch/admin/approved?secret=' + hc2_secret)
hc2_req.encoding = 'utf-8'
hc2_soup = BeautifulSoup(hc2_req.text, 'html.parser')


# Get the rows, except the first (header)
rows = hc2_soup.findAll('tr')[1:]

# Convert to teams
teams = {}
loc_idx = 0
for idx, row in enumerate(rows):
  cells = row.findAll('td')
  team_name = clean(cells[0].text)

  if team_name not in teams:
    team = {
      'user_name': 'hc2-' + str(idx),
      'name': team_name,
      'members': [],
      'category_id': dj_categ_pro if clean(cells[1].text) == 'professional' else dj_categ_student,
      'location': locations[loc_idx],
      'password': gen_password(),
      'extra': []
    }
    teams[team_name] = team
    loc_idx = loc_idx + 1
    print('Imported team ' + team_name)

  person_name = clean(cells[2].text)
  teams[team_name]['members'].append(person_name)
  teams[team_name]['extra'].append(clean(cells[5].text))
  print('Imported contestant ' + person_name)

# Output the file
with open('teams.json', 'w') as teams_file:
  json.dump({'teams': list(teams.values())}, teams_file, sort_keys=True, indent=4)


print('Done!')
