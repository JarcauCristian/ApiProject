from pprint import pprint
import requests

headers = {'Content-type': 'application/json'}
rsp = requests.get('http://147.102.33.214:8080/fhir/Patient?_id=100271&_revinclude=Observation:subject&_pretty=True', headers=headers)
pprint(rsp.json()['entry'][0])
