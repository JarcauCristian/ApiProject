import requests

for i in range(103896, 103910):
    rsp = requests.delete(f'http://147.102.33.214:8080/fhir/Observation?_id={i}', headers={"Content-Type": "application/json"})
    if rsp.status_code == 200:
        print("Success")
