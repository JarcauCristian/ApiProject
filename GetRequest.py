import json
from pprint import pprint

import requests

headers = {'Content-type': 'application/json'}
# rsp = requests.get('http://147.102.33.214:8080/fhir?_getpages=ac1ee897-b78f-4ab5-8f93-ca9fd969b60b&_getpagesoffset=40&_count=1500&_pretty=true&_bundletype=searchset', headers=headers)
# with open('data.json', 'w') as json_out:
#     json_out.write(json.dumps(rsp.json()))

# rsp = requests.get('http://147.102.33.214:8080/fhir?_getpages=afe8876e-d02e-4604-a5fb-7429db79683c&_getpagesoffset=7&_count=1500&_pretty=true&_bundletype=searchset', headers=headers)
# with open('condition_data.json', 'w') as json_out:
#     json_out.write(json.dumps(rsp.json()))

rsp = requests.get('http://147.102.33.214:8080/fhir/Patient?_getpagesoffset=13&_count=400&_pretty=true&_bundletype=searchset', headers=headers)

pprint(rsp.json()['entry'][0])
