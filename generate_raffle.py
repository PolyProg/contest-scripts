#!/usr/bin/python3
from bs4 import BeautifulSoup
import json
import os
import random
import requests
import sys


# Get the config
config_path = input('Config file path: ')
with open(config_path, encoding='utf-8') as config_file:
  config = json.load(config_file)


# Get teams to exclude
to_exclude_str = input('Team IDs to exclude, separated by commas: ').strip()
if len(to_exclude_str) > 0:
  to_exclude = set(map(lambda s: int(s.strip()), to_exclude_str.split(',')))
else:
  to_exclude = set()


# Validate data
to_exclude_clone = set(to_exclude)
if 'teams' not in config:
  sys.exit('Config must contain teams')
teams = config['teams']
for team in teams:
  if 'name' not in team or 'members' not in team or 'id' not in team:
    sys.exit('Teams must have name, members, id')
  if team['id'] in to_exclude:
    print('excluding ' + str(team['id']))
    to_exclude_clone.remove(team['id'])
if len(to_exclude_clone) > 0:
  sys.exit('Excluded IDs do not exist: ' + ', '.join(to_exclude_clone))

# Get the DOMJudge host & session
dj_url = input('DOMJudge base URL (no trailing slash): ')
dj_session = input('DOMJudge session cookie: ')


# Create cookies
dj_cookies = { 'domjudge_session': dj_session }


# Get scoreboard
score_req = requests.get(dj_url + '/api/scoreboard', cookies=dj_cookies)
score_req.raise_for_status()
score = json.loads(score_req.text)
print('Downloaded scoreboard')


# Load the number of problems solved per team
for score_team in score:
  team = next((t for t in teams if t['id'] == score_team['team']), None)
  if team is not None:
    team['solved'] = score_team['score']['num_solved']


# Check whether any teams weren't in the scoreboard
for team in teams:
  if 'solved' not in team:
      print('WARNING: Team without score: ' + team['name'])


# Generate the array of winners, with weighted probability
# To do so, clone people as many times as they have solved problems,
# then shuffle that array, and finally remove duplicates.
# Not very efficient, but len(teams) is <100...
winners = []
for team in teams:
  if team['id'] not in to_exclude:
    for member in team['members']:
      winners += [(member, team['name']) for i in range(max(1, team['solved']))]
random.shuffle(winners)
result = []
for winner in winners:
  if winner not in result:
    result.append(winner)


# Create the out directory now (there are 2 outputs)
os.makedirs('out', exist_ok=True)


# Print the winners to a file, for logging purposes
with open('out/raffle.log', 'w') as result_log:
  print('\n'.join([p[0] + ' | ' + p[1] for p in result]), file=result_log)


# Generate the HTML
result_array = '[\n' + ',\n'.join(['[' + json.dumps(p[0]) + ', ' + json.dumps(p[1]) + ']' for p in result]) + '\n]'
html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>Raffle</title>
  <style>
  #container {
    background-color: #fff;
  }

  h1 {
    font-size: 10em;
    font-weight: 700;
    text-align: center;
  }

  h2 {
    font-size: 5em;
    font-weight: 400;
    text-align: center;
  }

  #next {
    font-size: 2em;
    color: #B0B0B0;

    position: absolute;
    left: 2em;
    bottom: 2em;
  }

  #fullscreen {
    font-size: 2em;
    color: #F0F0F0;

    position: absolute;
    right: 2em;
    bottom: 2em;
  }
  </style>
  <script>
    RESULTS = """ + result_array + """;

    var index = 0;
    var isLoading = false;
    function showNext() {
      if(isLoading) {
        return;
      }
      isLoading = true;

      var title = document.getElementById('title');
      var subtitle = document.getElementById('subtitle');

      title.textContent = '';
      subtitle.textContent = '';

      if(index < RESULTS.length) {
        title.textContent = '.';
        setTimeout(function() {
          title.textContent = '. .';

          setTimeout(function() {
            title.textContent = '. . .';

            setTimeout(function() {
              title.textContent = RESULTS[index][0];
              subtitle.textContent = RESULTS[index][1];
              index++;
              isLoading = false;
            }, 1000);
          }, 1000);
        }, 1000);

      } else {
        subtitle.textContent = "there's nobody left!";
      }
    }

    function showFullscreen() {
      var container = document.getElementById('container');
      if('requestFullscreen' in container) {
        container.requestFullscreen();
      } else if ('webkitRequestFullscreen' in container) {
        container.webkitRequestFullscreen();
      } else if ('mozRequestFullScreen' in container) {
        container.mozRequestFullScreen();
      } else if ('msRequestFullscreen' in container) {
        container.msRequestFullscreen();
      }
    }
  </script>
</head>
<body>
  <div id="container">
    <h1 id="title">Raffle</h1>
    <h2 id="subtitle"></h2>
    <a id="next" href="#" onclick="showNext(); return false;">next</a>
    <a id="fullscreen" href="#" onclick="showFullscreen(); return false;">fullscreen</a>
  </div>
</body>
</html>
"""


# Print the HTML to a file
with open('out/raffle.html', 'w') as html_file:
  print(html, file=html_file)


print('Done!')
