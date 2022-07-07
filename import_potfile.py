
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
  try:
    ad_ntlm = str(line.split(':')[0])
    ad_password = str(line.split(':')[1])
    print("[+] importing "+ad_ntlm+" / "+ad_password)
    rolodata.update_crack(ad_ntlm, ad_password)
  except Exception as e:
    print('whoops '+str(e))

rolodata.commit()
