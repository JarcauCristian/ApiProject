import requests

for i in range(105428, 106923):
    rsp = requests.delete(f'http://147.102.33.214:8080/fhir/Condition?_id={i}', headers={"Content-Type": "application/json"})
    if rsp.status_code == 200:
        print("Success")
