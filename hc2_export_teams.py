#!/usr/bin/python3
from bs4 import BeautifulSoup
import json
import random
import re
import requests

def gen_password():
  password = ''
  for i in range(3):
    password += random.choice('abcdefghijklmnopqrstuvwxyz')
    password += random.choice('.!?')
    password += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    password += random.choice('0123456789')
  return password

def clean(s):
  return re.sub(' +',' ', s.strip())


# Get the category IDs
dj_categ_student = int(input('DOMJudge students category ID: '))
dj_categ_pro = int(input('DOMJudge professionals category ID: '))


# Get the session cookie
hc2_secret = input('HC2.ch secret: ')


# Get the teams list
hc2_req = requests.get('http://myhc2.azurewebsites.net/admin/approved?secret=' + hc2_secret)
hc2_req.encoding = 'utf-8'
hc2_soup = BeautifulSoup(hc2_req.text, 'html.parser')


# Get the rows, except the first (header)
rows = hc2_soup.findAll('tr')[1:]


# Convert to teams
teams = {}
for idx, row in enumerate(rows):
  cells = row.findAll('td')
  team_name = clean(cells[0].text)

  if team_name not in teams:
    team = {
      'user_name': 'hc2-' + str(idx),
      'name': team_name,
      'members': [],
      'category_id': dj_categ_pro if clean(cells[1].text) == 'professional' else dj_categ_student,
      'location': '',
      'password': gen_password(),
      'extra': []
    }
    teams[team_name] = team
    print('Imported team ' + team_name)

  person_name = clean(cells[2].text)
  teams[team_name]['members'].append(person_name)
  teams[team_name]['extra'].append(clean(cells[5].text))
  print('Imported contestant ' + person_name)

# Output the file
with open('teams.json', 'w') as teams_file:
  json.dump({'teams': list(teams.values())}, teams_file, sort_keys=True, indent=4)


print('Done!')
