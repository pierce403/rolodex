
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

bhuserfile = sys.argv[1]
with open(bhuserfile) as data_file:
  data = simplejson.load(data_file)

fields = ["name", "email", "enabled", "title", "displayname", "description"]

print ("name,enabled,displayname,email,title,description")
for i in data['users']:
  new_person = {}

  print("[+] importing "+str(i['Properties']['displayname']))
  for field in fields:
    new_person['ad_'+field] = i['Properties'][field]

  rolodata.new_person(new_person)

rolodata.commit()
