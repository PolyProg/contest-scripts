#!/usr/bin/python3
from bs4 import BeautifulSoup
import json
import re
import requests


def clean(s):
  return re.sub(' +',' ', s.strip())


# Get the category IDs
dj_categ_student = int(input('DOMJudge students category ID: '))
dj_categ_pro = int(input('DOMJudge professionals category ID: '))


# Get the session cookie
hc2_session = input('HC2.ch PHPSESSID: ')


# Create the cookies
hc2_cookies = { 'PHPSESSID': hc2_session }


# Get the teams list
hc2_req = requests.get('http://hc2.ch/admin/teams.php?all', cookies=hc2_cookies)
hc2_req.encoding = 'utf-8'
hc2_soup = BeautifulSoup(hc2_req.text, 'html.parser')


# Get the rows, except the first (header) and last (sum totals)
rows = hc2_soup.findAll('tr')[1:-1]


# Convert to teams
teams = []
for row in rows:
  cells = row.findAll('td')
  team_name = clean(cells[18].text)

  if cells[20].text == '1':
    print('Ignoring waiting list team ' + team_name)
  else:
    team = {
      'name': clean(cells[18].text),
      'members': list(map(clean, cells[2].text.split(','))),
      'category_id': dj_categ_pro if clean(cells[15].text) == '1' else dj_categ_student,
      'location': clean(cells[24].text),
      'password': clean(cells[39].text),
      'extra': ['t-shirts: ' + clean(cells[4].text)]
    }
    
    teams.append(team)
    print('Imported team ' + team_name)


# Output the file
with open('teams.json', 'w') as teams_file:
  json.dump({'teams': teams}, teams_file, sort_keys=True)


print('Done!')
