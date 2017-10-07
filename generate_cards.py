#!/usr/bin/python3
import json
import html
import os
import pdfkit
import sys


# Get the config
config_path = input('Config file path: ')
with open(config_path, encoding='utf-8') as config_file:
  config = json.load(config_file)


# Validate data
if 'teams' not in config:
  sys.exit('Config must contain teams')
teams = config['teams']
for team in teams:
  if 'name' not in team or \
     'user_name' not in team or 'password' not in team:
    sys.exit('Teams must have name, members, location, user_name, password')


# Sort teams by location, to ease the work of people putting cards on tables
teams.sort(key=lambda t: t['location'] if 'location' in teams else t['name'])


# Convert teams to an HTML table contents
table = ""
for idx, team in enumerate(teams):
  cell = ""

  cell += '<div style="page-break-inside: avoid;">'
  cell += '<h1>' + html.escape(team['name']) + '</h1>'
  if 'members' in team:
    cell += '<h2>' + html.escape(', '.join(team['members'])) + '</h2>'
  cell += '<div>'
  cell += 'DOMJudge username: <span class="cred">' + team['user_name'] + '</span>'
  cell += '<br>'
  cell += 'DOMJudge password: <span class="cred">' + team['password'] + '</span>'
  cell += '</div>'
  cell += '<h3>'
  if 'location' in team:
    cell += 'loc: ' + team['location']
  if 'extra' in team:
    cell += ' / ' + ' / '.join(team['extra'])
  cell += '</h3>'
  cell += '</div>'

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
    font-weight: 700;
  }

  h2 {
    font-size: 1.2em;
    font-weight: 500;
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
<body>""" + table + """</body>
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
os.makedirs('out', exist_ok=True)
pdfkit.from_string(html, 'out/cards.pdf', options=options)

print('Done!')
