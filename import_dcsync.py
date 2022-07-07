
print('oh hai')
import sys
import simplejson

# shoutz bloodhound-users-json-parser.py

import rolodex
import rolodata
app = rolodex.app
app.app_context().push()

if len(sys.argv) == 1:
  print ("Usage: " + sys.argv[0] + " dcsync.ntds")
  sys.exit()

ntdsfile = sys.argv[1]
data =  open(ntdsfile).readlines()

updates = []

for line in data:
  new_person = {}
  print(line)
  ntds_name = line.split(':')[0]
  name_ary = ntds_name.split('\\')
  print(name_ary)
  try:
    new_person['ad_name'] = str(name_ary[1]+'@'+name_ary[0]).upper()
    new_person['ad_ntlm'] = str(line.split(':')[3])
    #updates.append(new_person)
    #rolodata.bulk_update(new_person)
    rolodata.update_hash(new_person['ad_name'], new_person['ad_ntlm'])
  except Exception as e:
    print('whoops '+str(e))
  print(new_person)

#rolodata.bulk_update(updates)
rolodata.commit()
