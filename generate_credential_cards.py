#!/usr/bin/python3
import json
import pdfkit


# Get the config
config_path = input('Config file path: ')
with open(config_path, encoding='utf-8') as config_file:
  config = json.load(config_file)


# Validate data
if 'teams' not in config:
  sys.exit('Config must contain teams')
teams = config['teams']
for team in teams:
  if 'name' not in team or 'members' not in team or 'location' not in team or \
     'user_name' not in team or 'password' not in team or \
     'id' not in team or 'user_id' not in team:
    sys.exit('Teams must have name, members, location, user_name, password, id, user_id')


# Convert teams to an HTML table contents
table = ""
for idx, team in enumerate(config['teams']):
  cell = ""

  if idx % 2 == 0:
      cell += '<tr>'

  cell += '<td>'
  cell += '<h1>' + team['name'] + '</h1>'
  cell += '<h2>' + ', '.join(team['members']) + '</h2>'
  cell += '<div>'
  cell += 'DOMJudge username: <span class="cred">' + team['user_name'] + '</span>'
  cell += '<br>'
  cell += 'DOMJudge password: <span class="cred">' + team['password'] + '</span>'
  cell += '</div>'
  cell += '<h3>(info for organizers: loc ' + team['location'] + ' / id ' + str(team['id']) + ' / uid ' + str(team['user_id']) + ')</h3>'
  cell += '</td>'

  if idx % 2 == 1:
      cell += '</tr>'
  
  table += cell


# Create the HTML
html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <style>
  table {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    border-collapse: collapse;
  }

  td {
    margin: 0;
    padding: 0;
    width: 50%;
  }

  h1 {
    font-size: 1.8em;
    font-weight: bold;
  }

  h2 {
    font-size: 1.2em;
    font-weight: semibold;
  }

  div {
    font-size: 1.2em;
  }

  .cred {
    font-family: monospace;
  }

  h3 {
    font-size: 0.7em;
    font-weight: normal;
  }
  </style>
</head>
<body>
  <table>""" + table + """</table>
</body>
</html>
"""


# Set options (notably, A4 paper, and margins equivalent to MS Word's "narrow")
options = {
    'page-size': 'A4',
    'margin-top': '0.5in',
    'margin-right': '0.5in',
    'margin-bottom': '0.5in',
    'margin-left': '0.5in',
    'encoding': 'UTF-8'
}


# Output the PDF
print('Outputting PDF, this may take a while...')
pdfkit.from_string(html, 'credential_cards.pdf', options=options)


print('Done!')
