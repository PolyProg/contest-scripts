#!/usr/bin/python3
from bs4 import BeautifulSoup
import json
import math
import requests
import time
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
  if 'name' not in team or 'password' not in team:
    sys.exit('Teams must have name, password')
  if 'location' in team:
    if team['location'] in all_locs:
      sys.exit('Duplicate location found: ' + team['location'])
    all_locs.add(team['location'])


# Get the DOMJudge host & session
dj_url = input('DOMJudge base URL (no trailing slash): ')
dj_session = input('DOMJudge session cookie: ')


# Create cookies
dj_cookies = { 'domjudge_session': dj_session }


# Get teams, to check whether they already exist
check_teams_req = requests.get(dj_url + '/jury/teams.php', cookies=dj_cookies)
check_teams_soup = BeautifulSoup(check_teams_req.text, 'html.parser')

already_done = []

def fix(name):
  return name.replace("'", "&apos;")

# Create teams
for idx, team in enumerate(teams):
  if check_teams_soup.find(text=fix(team['name'])) is not None:
    print('Team already exists: ' + team['name'])
    already_done.append(team['name'])
    continue

  team_form = {
    'data[0][name]': team['name'],
    'data[0][categoryid]': team['category_id'], # 2 == default "self-registered",
    'data[0][room]': team['location'] if 'location' in team else '',
    'data[0][mapping][1][extra][username]': team['user_name'],
    'cmd': 'add',
    'referrer': '',
    'table': 'team',
    'data[0][adduser]': '1',
    'data[0][affilid]': '',
    'data[0][comments]': '',
    'data[0][enabled]': '1',
    'data[0][penalty]': '0',
    'data[0][members]': '',
    'data[0][mapping][0][fk][0]': 'teamid',
    'data[0][mapping][0][fk][1]': 'cid',
    'data[0][mapping][0][table]': 'contestteam',
    'data[0][mapping][1][fk]': 'teamid',
    'data[0][mapping][1][table]': 'user'
  }
  r = requests.post(dj_url + '/jury/edit.php', cookies=dj_cookies, data=team_form)
  r.raise_for_status()
  print('Created team ' + team['name'])
  time.sleep(0.5)


# Get team IDs (using their name)
teams_req = requests.get(dj_url + '/jury/teams.php', cookies=dj_cookies)
teams_soup = BeautifulSoup(teams_req.text, 'html.parser')
for team in teams:
  # find the location, then its parent the <a> tag, then its parent the <td>,
  # then its parent the <tr>
  loc = teams_soup.find(text=fix(team['name']))
  if loc is None: sys.exit("wtf " + fix(team['name']))
  tr = loc.parent.parent.parent
  # first td contains the team ID as text, prefixed with 't'
  team['id'] = int(list(tr.children)[0].string[1:])


# Get team user IDs (using their name)
users_req = requests.get(dj_url + '/jury/users.php', cookies=dj_cookies)
users_soup = BeautifulSoup(users_req.text, 'html.parser')
for team in teams:
  # find the username, then its parent the <a> tag
  a = users_soup.find(text=team['user_name']).parent
  # href contains the ID at the end, after a '='
  team['user_id'] = int(a['href'][a['href'].index('=') + 1:])


# Edit users (to set their password)
for team in teams:
  user_form = {
    'data[0][teamid]': team['id'],
    'data[0][name]': team['name'],
    'keydata[0][userid]': team['user_id'],
    'keydata[0][username]': team['user_name'],
    'data[0][password]': team['password'],
    'data[0][email]': '',
    'data[0][enabled]': '1',
    'data[0][ip_address]': '',
    'data[0][mapping][0][items][2]': '3',
    'cmd': 'edit',
    'referrer': '',
    'table': 'user',
    'data[0][mapping][0][fk][0]': 'userid',
    'data[0][mapping][0][fk][1]': 'roleid',
    'data[0][mapping][0][table]': 'userrole'
  }
  r = requests.post(dj_url + '/jury/edit.php', cookies=dj_cookies, data=user_form)
  r.raise_for_status()
  print('Edited user for ' + team['name'])
  time.sleep(0.5)


# Update the file to include teams' IDs and user IDs
with open(config_path, 'w') as config_file:
    json.dump(config, config_file, sort_keys=True)
print('File updated with team IDs and user IDs')


print('Done!')
