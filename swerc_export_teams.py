#!/usr/bin/python3
from bs4 import BeautifulSoup
import json
import re
import requests


def clean(s):
  return re.sub(' +',' ', s.strip())


# Get the affiliation IDs
dj_affil_epf = int(input('DOMJudge EPFL affiliation ID: '))
dj_affil_eth = int(input('DOMJudge ETHZ affiliation ID: '))


# Get the session cookie
hc2_session = input('swerc.hc2.ch PHPSESSID: ')


# Create the cookies
hc2_cookies = { 'PHPSESSID': hc2_session }


# Get the teams list
hc2_req = requests.get('http://swerc.hc2.ch/admin/index.php?all', cookies=hc2_cookies)
hc2_req.encoding = 'utf-8'
hc2_soup = BeautifulSoup(hc2_req.text, 'html.parser')

# Get the rows, except the first (header) and last (sum totals)
rows = hc2_soup.findAll('tr')[1:-1]

# Convert to teams
teams = []
for row in rows:
  cells = row.findAll('td')

  affil = None
  affil_text = clean(cells[7].text)
  if affil_text == "EPFL":
    affil = dj_affil_epf
  elif affil_text == "ETH":
    affil = dj_affil_eth

  team = {
    'login': clean(cells[0].text),
    'name': clean(cells[3].text) + " " + clean(cells[4].text),
    'affiliation_id': affil,
    'password': clean(cells[8].text),
    'eligible': True if clean(cells[14].text) == '1' else False
  }
    
  teams.append(team)
  print('Imported ' + team['name'])


# Output the file
with open('teams.json', 'w') as teams_file:
  json.dump({'teams': teams}, teams_file, sort_keys=True)


print('Done!')
