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
  if 'name' not in team or 'members' not in team or 'location' not in team :
    sys.exit('Teams must have name, members, location')


# Convert teams to HTML divs
body = ""
for idx, team in enumerate(config['teams']):
  div = ""

  # don't put a page break on the last page, to avoid a blank sheet at the end
  if idx < len(config['teams']) - 1:
    div += '<div style="page-break-after: always;">'
  else:
    div += '<div>'

  div += '<h1>' + team['name'] + '</h1>'
  div += '<h2>' + ', '.join(team['members']) + '</h2>'
  div += '<h3>' + team['location'] + '</h3>'
  div += '</div>'

  body += div


# Create the HTML
html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <style>
  h1 {
    font-size: 10em;
    font-weight: 700;
  }
  
  h2 {
    font-size: 4em;
    font-weight: 500;
  }

  h3 {
    font-size: 1em;
    font-weight: normal;
  }
  </style>
</head>
<body>""" + body + """</body>
</html>
"""


# Set options (notably, A4 paper, and margins equivalent to MS Word's "narrow")
options = {
    'orientation': 'landscape',
    'page-size': 'A4',
    'margin-top': '0.5in',
    'margin-right': '0.5in',
    'margin-bottom': '0.5in',
    'margin-left': '0.5in',
    'encoding': 'UTF-8'
}


# Output the PDF
print('Outputting PDF, this may take a while...')
pdfkit.from_string(html, 'panels.pdf', options=options)


print('Done!')
