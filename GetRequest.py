<<<<<<< HEAD
=======
import csv
from datetime import datetime
>>>>>>> af417752bbce89cc9724261c20719d9ac7a9812d
import requests

headers = {'Content-type': 'application/json'}

<<<<<<< HEAD
# with open('observation-data.json', 'r') as json_in:
#     json_data = json_in.read()
#
# data = json.loads(json_data)
#
# for i in data['entry']:
#     i['resource']['effectiveDateTime'] = '2022-08' + i['resource']['effectiveDateTime'][7:]
#     i['resource']['issued'] = '2022-08' + i['resource']['effectiveDateTime'][7:]
#     rsp = requests.put(f'http://147.102.33.214:8080/fhir/Observation/{int(i["resource"]["id"])}?_format=json&_pretty=true', headers=headers, data=json.dumps(i['resource']))
#
#     if rsp.status_code == 200:
#         print('Success')
#     sleep(2)

rsp = requests.get('http://147.102.33.214:8080/fhir/Condition?_getpagesoffset=7&_count=1502&_pretty=true&_bundletype=searchset', headers=headers)
if rsp.status_code == 200:
    for i in rsp.json()['entry']:
        if i['resource']['recordedDate'][:7] != '2022-08':
            print('The date dose not match!')
=======
# Observations
CPK = []
Platelets = []
Creatinine = []
Sodium = []
Ejection_Fraction = []
Date_Death = []

# Conditions
Anaemia = []
Diabetes = []
Smoker = []
Arterial_Hypertension = []
Death = []

# Patient
Age = []
Gender = []


for bundle in range(100271, 100570):
    rsp = requests.get(
        f'http://147.102.33.214:8080/fhir/Patient?_id={bundle}&_revinclude=Observation:subject&_revinclude=Condition:subject&_pretty=True',
        headers=headers)
    Age.append(datetime.now().year - int(rsp.json()['entry'][0]['resource']['birthDate'][:4]))
    if rsp.json()['entry'][0]['resource']['gender'] == 'female':
        Gender.append(0)
    else:
        Gender.append(1)

    for entry in range(1, 12):
        match rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display']:
            case "Creatinine Phosphokinase":
                CPK.append(rsp.json()['entry'][entry]['resource']['valueQuantity']['value'])
            case "Platelets":
                Platelets.append(rsp.json()['entry'][entry]['resource']['valueQuantity']['value'])
            case "Creatinine":
                Creatinine.append(rsp.json()['entry'][entry]['resource']['valueQuantity']['value'])
            case "Sodium":
                Sodium.append(rsp.json()['entry'][entry]['resource']['valueQuantity']['value'])
            case "Ejection Fraction":
                Ejection_Fraction.append(rsp.json()['entry'][entry]['resource']['valueQuantity']['value'])
            case "Date Death":
                Date_Death.append(rsp.json()['entry'][entry]['resource']['valueQuantity']['value'])
            case "Anaemia":
                if rsp.json()['entry'][entry]['resource']['clinicalStatus']['coding'][0]['code'] == "inactive":
                    Anaemia.append(0)
                else:
                    Anaemia.append(1)
            case "Diabetes":
                if rsp.json()['entry'][entry]['resource']['clinicalStatus']['coding'][0]['code'] == "inactive":
                    Diabetes.append(0)
                else:
                    Diabetes.append(1)
            case "Smoker":
                if rsp.json()['entry'][entry]['resource']['clinicalStatus']['coding'][0]['code'] == "inactive":
                    Smoker.append(0)
                else:
                    Smoker.append(1)
            case "Arterial Hypertension":
                if rsp.json()['entry'][entry]['resource']['clinicalStatus']['coding'][0]['code'] == "inactive":
                    Arterial_Hypertension.append(0)
                else:
                    Arterial_Hypertension.append(1)
            case "Death":
                if rsp.json()['entry'][entry]['resource']['clinicalStatus']['coding'][0]['code'] == "inactive":
                    Death.append(0)
                else:
                    Death.append(1)

with open('my-heart-failure.csv', 'w', newline='') as csv_out:
    csv_writer = csv.writer(csv_out)
    csv_writer.writerow(
        ['TIME', 'Event', 'Gender', 'Smoking', 'Diabetes', 'BP', 'Anaemia', 'Age', 'Ejection.Fraction', 'Sodium', 'Creatinine',
         'Platelets', 'CPK'])
    for j in range(0, 299):
        row = [Date_Death[j], Death[j], Gender[j], Smoker[j], Diabetes[j], Arterial_Hypertension[j], Anaemia[j], Age[j],
               Ejection_Fraction[j], Sodium[j], Creatinine[j], Platelets[j], CPK[j]]
        csv_writer.writerow(row)
>>>>>>> af417752bbce89cc9724261c20719d9ac7a9812d
