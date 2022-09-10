# Get the observation from the api call:
def get_data_observation(rsp):
    cpk = [rsp.json()['entry'][i]['resource']['component'][0]['valueQuantity']['value'] for i in
           range(0, 299)]  # CPK observation
    plt = [rsp.json()['entry'][i]['resource']['component'][0]['valueQuantity']['value'] for i in
           range(299, 598)]  # Platelets observation
    ejf = [rsp.json()['entry'][i]['resource']['component'][0]['valueQuantity']['value'] for i in
           range(598, 897)]  # Creatinine observation
    ddh = [rsp.json()['entry'][i]['resource']['component'][0]['valueQuantity']['value'] for i in
           range(897, 1196)]  # Sodium observation
    crt = [rsp.json()['entry'][i]['resource']['component'][0]['valueQuantity']['value'] for i in
           range(1196, 1495)]  # Ejection_Fraction observation
    sod = [rsp.json()['entry'][i]['resource']['component'][0]['valueQuantity']['value'] for i in
           range(1495, 1794)]  # Date_Death observation

    return cpk, plt, crt, sod, ejf, ddh


# Get the conditions from the api call:
def get_data_condition(rsp):
    anm = []  # Anemia condition
    dbt = []  # Diabetes condition
    smk = []  # Smoker condition
    arh = []  # Arterial_Hypertension condition
    dth = []  # Death condition

    for i in range(0, 299):
        if rsp.json()['entry'][i]['resource']['clinicalStatus']['coding'][0]['code'] == 'inactive':
            anm.append(0)
        else:
            anm.append(1)

    for i in range(299, 598):
        if rsp.json()['entry'][i]['resource']['clinicalStatus']['coding'][0]['code'] == 'inactive':
            dbt.append(0)
        else:
            dbt.append(1)

    for i in range(598, 897):
        if rsp.json()['entry'][i]['resource']['clinicalStatus']['coding'][0]['code'] == 'inactive':
            smk.append(0)
        else:
            smk.append(1)

    for i in range(897, 1196):
        if rsp.json()['entry'][i]['resource']['clinicalStatus']['coding'][0]['code'] == 'inactive':
            arh.append(0)
        else:
            arh.append(1)

    for i in range(1194, 1493):
        if rsp.json()['entry'][i]['resource']['clinicalStatus']['coding'][0]['code'] == 'inactive':
            dth.append(0)
        else:
            dth.append(1)

    return anm, dbt, smk, arh, dth


# Get the patients from the api call:
def get_data_patient(rsp):
    patients = [rsp]
    age = []
    gender = []
    for i in range(0, 299):
        age.append(int(datetime.now().year) - int(patients[0][i]['entry'][0]['resource']['birthDate'][:4]))
        if patients[0][i]['entry'][0]['resource']['gender'] == 'female':
            gender.append(0)
        else:
            gender.append(1)

    return age, gender


import csv
from datetime import datetime
import requests

# Headers for the api request-call
headers = {'Content-type': 'application/json'}

# Insert the observations that are coming from the api.
rsp_obs = requests.get(
    'http://147.102.33.214:8080/fhir/Observation?_getpagesoffset=51&_count=1845&_pretty=true&_bundletype=searchset',
    headers=headers)
CPK = get_data_observation(rsp_obs)[0]
Platelets = get_data_observation(rsp_obs)[1]
Creatinine = get_data_observation(rsp_obs)[2]
Sodium = get_data_observation(rsp_obs)[3]
Ejection_Fraction = get_data_observation(rsp_obs)[4]
Date_Death = get_data_observation(rsp_obs)[5]

# Insert the conditions that are coming from the api.
rsp_cond = requests.get(
    'http://147.102.33.214:8080/fhir/Condition?_getpagesoffset=7&_count=1502&_pretty=true&_bundletype=searchset',
    headers=headers)
Anemia = get_data_condition(rsp_cond)[0]
Diabetes = get_data_condition(rsp_cond)[1]
Smoker = get_data_condition(rsp_cond)[2]
Arterial_Hypertension = get_data_condition(rsp_cond)[3]
Death = get_data_condition(rsp_cond)[4]

# Insert the patients that are coming from the api
rsp_pat = []

for pts in range(100271, 100570):
    rsp_pats = requests.get(f'http://147.102.33.214:8080/fhir/Patient?_id={pts}&_pretty=true', headers=headers)
    rsp_pat.append(rsp_pats.json())

Age = get_data_patient(rsp_pat)[0]
Gender = get_data_patient(rsp_pat)[1]

with open('my-heart-failure.csv', 'w', newline='') as csv_out:
    csv_writer = csv.writer(csv_out)
    csv_writer.writerow(
        ['TIME', 'Event', 'Gender', 'Smoking', 'Diabetes', 'BP', 'Anaemia', 'Age', 'Ejection.Fraction', 'Sodium',
         'Creatinine',
         'Platelets', 'CPK'])
    for j in range(0, 299):
        row = [Date_Death[j], Death[j], Gender[j], Smoker[j], Diabetes[j], Arterial_Hypertension[j], Anemia[j], Age[j],
               Ejection_Fraction[j], Sodium[j], Creatinine[j], Platelets[j], CPK[j]]
        csv_writer.writerow(row)
