import csv
import json
from time import sleep
from pprint import pprint
import requests

headers = {'Content-type': 'application/json'}

with open('JSONFiles/patients.json', 'r') as json_in:
    json_data = json_in.read()

data = json.loads(json_data)

with open('gender.csv') as csv_in:
    csv_reader = csv.reader(csv_in)

    gender = []

    for i, value in enumerate(csv_reader):
        if i == 0:
            continue
        gender.append(value[0])

for i in range(0, 299):
    if gender[i] == '1':
        data['entry'][i]['resource']['gender'] = 'male'
    else:
        data['entry'][i]['resource']['gender'] = 'female'

    rsp = requests.put(f'http://147.102.33.214:8080/fhir/Patient/{int(data["entry"][i]["resource"]["id"])}?_format=json&_pretty=true', headers=headers, data=json.dumps(data['entry'][i]['resource']))

    if rsp.status_code == 200:
        print('Success')
    sleep(2)
