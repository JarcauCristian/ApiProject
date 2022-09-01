import csv
from datetime import datetime

import requests

headers = {'Content-type': 'application/json'}

rsp_obs = requests.get(
    'http://147.102.33.214:8080/fhir/Observation?_getpagesoffset=51&_count=1546&_pretty=true&_bundletype=searchset',
    headers=headers)

CPK = [rsp_obs.json()['entry'][i]['resource']['component'][0]['valueQuantity']['value'] for i in range(0, 299)]
Platelets = [rsp_obs.json()['entry'][i]['resource']['component'][0]['valueQuantity']['value'] for i in range(299, 598)]
Creatinine = [rsp_obs.json()['entry'][i]['resource']['component'][0]['valueQuantity']['value'] for i in range(598, 897)]
Sodium = [rsp_obs.json()['entry'][i]['resource']['component'][1]['valueQuantity']['value'] for i in range(598, 897)]
Ejection_Fraction = [rsp_obs.json()['entry'][i]['resource']['component'][0]['valueQuantity']['value'] for i in range(897, 1196)]
Date_Death = [rsp_obs.json()['entry'][i]['resource']['component'][0]['valueQuantity']['value'] for i in range(1196, 1495)]

rsp_cond = requests.get('http://147.102.33.214:8080/fhir/Condition?_getpagesoffset=7&_count=1502&_pretty=true&_bundletype=searchset', headers=headers)

Anemia = []
Diabetes = []
Smoker = []
Arterial_Hypertension = []
Death = []

for i in range(0, 299):
    if rsp_cond.json()['entry'][i]['resource']['clinicalStatus']['coding'][0]['code'] == 'inactive':
        Anemia.append(0)
    else:
        Anemia.append(1)

for i in range(299, 598):
    if rsp_cond.json()['entry'][i]['resource']['clinicalStatus']['coding'][0]['code'] == 'inactive':
        Diabetes.append(0)
    else:
        Diabetes.append(1)

for i in range(598, 897):
    if rsp_cond.json()['entry'][i]['resource']['clinicalStatus']['coding'][0]['code'] == 'inactive':
        Smoker.append(0)
    else:
        Smoker.append(1)

for i in range(897, 1196):
    if rsp_cond.json()['entry'][i]['resource']['clinicalStatus']['coding'][0]['code'] == 'inactive':
        Arterial_Hypertension.append(0)
    else:
        Arterial_Hypertension.append(1)

for i in range(1194, 1493):
    if rsp_cond.json()['entry'][i]['resource']['clinicalStatus']['coding'][0]['code'] == 'inactive':
        Death.append(0)
    else:
        Death.append(1)

rsp_pat = []

for pts in range(100271, 100570):
    rsp = requests.get(f'http://147.102.33.214:8080/fhir/Patient?_id={pts}&_pretty=true', headers=headers)
    rsp_pat.append(rsp.json())

patients = [rsp_pat]
Age = []
Gender = []
for i in range(0, 299):
    Age.append(int(datetime.now().year) - int(patients[0][i]['entry'][0]['resource']['birthDate'][:4]))
    if patients[0][i]['entry'][0]['resource']['gender'] == 'female':
        Gender.append(0)
    else:
        Gender.append(1)

with open('heart-failure.csv', 'w', newline='') as csv_out:
    csv_writer = csv.writer(csv_out)
    csv_writer.writerow(
        ['TIME', 'Event', 'Gender', 'Smoking', 'Diabetes', 'BP', 'Anaemia', 'Age', 'Ejection.Fraction', 'Sodium', 'Creatinine',
         'Platelets', 'CPK'])
    for j in range(0, 299):
        row = [Date_Death[j], Death[j], Gender[j], Smoker[j], Diabetes[j], Arterial_Hypertension[j], Anemia[j], Age[j],
               Ejection_Fraction[j], Sodium[j], Creatinine[j], Platelets[j], CPK[j]]
        csv_writer.writerow(row)
