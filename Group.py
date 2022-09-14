import json
import requests

with open('Group.json', 'r') as json_in:
    json_data = json_in.read()

data = json.loads(json_data)

for i in range(100271, 100570):
    data['member'].append({'entity': {'reference': f'Patient/{i}'}})

rsp = requests.post('http://147.102.33.214:8080/fhir/Group?_format=json&_pretty=true', headers={'Content-Type': 'application/json'}, data=json.dumps(data))

if rsp.status_code == 201:
    print("Success!")
