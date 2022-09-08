from time import sleep
import requests
import json

headers = {"Content-Type": "application/json"}

with open('observation_data.json', 'r') as json_in:
    json_data = json_in.read()

data = json.loads(json_data)
for _, value in enumerate(data['entry']):
    value['resource']['valueQuantity'] = value['resource']['component'][0]['valueQuantity']
    del value['resource']['component']

    rsp = requests.put(f'http://147.102.33.214:8080/fhir/Observation/{int(value["resource"]["id"])}?_format=json&_pretty=true', headers=headers, data=json.dumps(value['resource']))

    if rsp.status_code == 200:
        print('Success')
    sleep(2)
