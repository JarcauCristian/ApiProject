import csv
from datetime import datetime
import requests

headers = {'Content-type': 'application/json'}

# Patient
Age = []
Gender = []

# Observations
cpk_list = list()
plt_list = list()
crt_list = list()
sod_list = list()
ejf_list = list()
dth_list = list()

# Conditions
Anaemia = []
Diabetes = []
Smoker = []
Arterial_Hypertension = []
Death = []

for bundle in range(100271, 100569, 2):
    rsp = requests.get(
        f'http://147.102.33.214:8080/fhir/Patient?_id={bundle}&_revinclude=Observation:subject&_revinclude=Condition:subject&_pretty=True',
        headers=headers)
    Age.append(datetime.now().year - int(rsp.json()['entry'][0]['resource']['birthDate'][:4]))
    if rsp.json()['entry'][0]['resource']['gender'] == 'female':
        Gender.append(0)
    else:
        Gender.append(1)

    CPK = {}
    Platelets = {}
    Creatinine = {}
    Sodium = {}
    Ejection_Fraction = {}
    Date_Death = {}

    for entry, _ in enumerate(rsp.json()['entry']):
        if entry == 0:
            continue
        if rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display'] == "Creatinine Phosphokinase":
            CPK[rsp.json()['entry'][entry]['resource']['effectiveDateTime'][:7]] = rsp.json()['entry'][entry]['resource']['valueQuantity']['value']
        elif rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display'] == "Platelets":
            Platelets[rsp.json()['entry'][entry]['resource']['effectiveDateTime'][:7]] = rsp.json()['entry'][entry]['resource']['valueQuantity']['value']
        elif rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display'] == "Creatinine":
            Creatinine[rsp.json()['entry'][entry]['resource']['effectiveDateTime'][:7]] = rsp.json()['entry'][entry]['resource']['valueQuantity']['value']
        elif rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display'] == "Sodium":
            Sodium[rsp.json()['entry'][entry]['resource']['effectiveDateTime'][:7]] = rsp.json()['entry'][entry]['resource']['valueQuantity']['value']
        elif rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display'] == "Ejection Fraction":
            Ejection_Fraction[rsp.json()['entry'][entry]['resource']['effectiveDateTime'][:7]] = rsp.json()['entry'][entry]['resource']['valueQuantity']['value']
        elif rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display'] == "Date Death":
            Date_Death['2022-08'] = rsp.json()['entry'][entry]['resource']['valueQuantity']['value']
        elif rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display'] == "Anaemia":
            if rsp.json()['entry'][entry]['resource']['clinicalStatus']['coding'][0]['code'] == "inactive":
                Anaemia.append(0)
            else:
                Anaemia.append(1)
        elif rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display'] == "Diabetes":
            if rsp.json()['entry'][entry]['resource']['clinicalStatus']['coding'][0]['code'] == "inactive":
                Diabetes.append(0)
            else:
                Diabetes.append(1)
        elif rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display'] == "Smoker":
            if rsp.json()['entry'][entry]['resource']['clinicalStatus']['coding'][0]['code'] == "inactive":
                Smoker.append(0)
            else:
                Smoker.append(1)
        elif rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display'] == "Arterial Hypertension":
            if rsp.json()['entry'][entry]['resource']['clinicalStatus']['coding'][0]['code'] == "inactive":
                Arterial_Hypertension.append(0)
            else:
                Arterial_Hypertension.append(1)
        elif rsp.json()['entry'][entry]['resource']['code']['coding'][0]['display'] == "Death":
            if rsp.json()['entry'][entry]['resource']['clinicalStatus']['coding'][0]['code'] == "inactive":
                Death.append(0)
            else:
                Death.append(1)

    cpk_list.append(CPK)
    plt_list.append(Platelets)
    crt_list.append(Creatinine)
    sod_list.append(Sodium)
    ejf_list.append(Ejection_Fraction)
    dth_list.append(Date_Death['2022-08'])

for i in cpk_list[0].keys():
    with open(f'heart-failure_{i}.csv', 'w', newline='') as csv_out:
        csv_writer = csv.writer(csv_out)
        csv_writer.writerow(
            ['TIME', 'Event', 'Gender', 'Smoking', 'Diabetes', 'BP', 'Anaemia', 'Age', 'Ejection.Fraction', 'Sodium', 'Creatinine',
             'Platelets', 'CPK'])
        for j in range(0, 149):
            row = [dth_list[j], Death[j], Gender[j], Smoker[j], Diabetes[j], Arterial_Hypertension[j], Anaemia[j], Age[j],
                   ejf_list[j][i], sod_list[j][i], crt_list[j][i], plt_list[j][i], cpk_list[j][i]]
            csv_writer.writerow(row)
