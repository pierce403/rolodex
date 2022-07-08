
print('oh hai')
import sys
import simplejson

# shoutz bloodhound-users-json-parser.py

import rolodex
import rolodata
app = rolodex.app
app.app_context().push()

if len(sys.argv) == 1:
  print ("Usage: " + sys.argv[0] + " bloodhound_users.json")
  sys.exit()

datafile = sys.argv[1]
with open(datafile) as data_file:
  data = simplejson.load(data_file)

fields = ["name", "email", "enabled", "title", "displayname", "description"]

if data:
  for person in data['profiles']:
    new_person = {}
    new_person['full_name'] = person['name']
    new_person['linkedin_url'] = person['linkedin_url']
    new_person['current_title'] = person['current_title']
    print('[+] importing '+new_person['full_name'])
    rolodata.new_person(new_person)

rolodata.commit()


