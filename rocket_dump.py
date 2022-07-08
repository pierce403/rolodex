import requests
import time
import os, sys

endpoint = 'https://api.rocketreach.co/v2/api/search'
key = os.getenv('ROCKETKEY')

# for example 'http://www.facebook.com/careers'
website = sys.argv[1]

headers = {'Api-Key':key, 'Content-Type': 'application/json'}

next_page = 1

while True:
  data = f'{{"query":{{"company_website_url": ["{website}"]}}, "start": {next_page}, "page_size": 100}}'
  print('posting request..')
  response = requests.post(endpoint, data=data, headers=headers)
  f = open(website.split('/')[2]+'-'+str(next_page)+".json", "w")
  f.write(response.text)
  f.close()

  result = response.json()
  if 'detail' in result.keys():
    print(result['detail'])
    if 'throttled' in result['detail']:
      sleeptime = int(result['detail'].split(' ')[6])
      print('sleeping for '+str(sleeptime+1)+' seconds..')
      time.sleep(sleeptime+1)

  if 'pagination' in result.keys():
    print(result['pagination'])
    next_page = int(result['pagination']['next'])
    if next_page > int(result['pagination']['total']):
      break
