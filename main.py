import csv
import json
import random
from datetime import datetime
from time import sleep
import requests


with open("JSONFiles/request.json", 'r') as json_in:
    json_data = json_in.read()

Headers = {"Content-Type": "application/json"}

with open("patients_2.csv", 'r') as csv_in:
    csv_data = csv.reader(csv_in)

    patients = list()
    for row in csv_data:
        patients.append(row)

with open("heart.csv", 'r') as csv_in:
    csv_data = csv.reader(csv_in)

    hrt = list()
    for row in csv_data:
        hrt.append(row)

hrt.pop(0)
data = json.loads(json_data)


def match_country(string: str):
    match string:
        case 'RO':
            return [44.439663, 26.096306]
        case 'AL':
            return [41.327953, 19.819025]
        case 'AT':
            return [48.210033, 16.363449]
        case 'BE':
            return [50.872986, 4.309333]
        case 'BG':
            return [42.698334, 23.319941]
        case 'HR':
            return [45.815399, 15.966568]
        case 'CY':
            return [35.185566, 33.382275]
        case 'CZ':
            return [50.073658, 14.418540]
        case 'DK':
            return [55.676098, 12.568337]
        case 'EE':
            return [59.436962, 24.753574]
        case 'FI':
            return [60.192059, 24.945831]
        case 'FR':
            return [48.864716, 2.349014]
        case 'DE':
            return [52.520008, 13.404954]
        case 'HU':
            return [47.497913, 19.040236]
        case 'IS':
            return [64.128288, -21.827774]
        case 'IE':
            return [53.350140, -6.266155]
        case 'IT':
            return [41.902782, 12.496366]
        case 'LV':
            return [56.946285, 24.105078]
        case 'LI':
            return [47.167500, 9.510530]
        case 'LT':
            return [54.687157, 25.279652]
        case 'LU':
            return [49.611622, 6.131935]
        case 'MK':
            return [41.177834, 20.678326]
        case 'MT':
            return [35.884445, 14.506944]
        case 'ME':
            return [42.442574, 19.268646]
        case 'NL':
            return [52.371807, 4.896029]
        case 'NO':
            return [59.911491, 10.757933]
        case 'PL':
            return [52.237049, 21.017532]
        case 'PT':
            return [38.736946, -9.142685]
        case 'RS':
            return [44.787197, 20.457273]
        case 'SK':
            return [48.148598, 17.107748]
        case 'SI':
            return [46.056946, 14.505751]
        case 'ES':
            return [40.416775, -3.703790]
        case 'SE':
            return [59.334591, 18.063240]
        case 'CH':
            return [46.947456, 7.451123]
        case 'TR':
            return [39.925533, 32.866287]
        case 'GB':
            return [51.503399, -0.119519]
        case 'GR':
            return [37.983810, 23.727539]
        case _:
            return None


def match_gender(gender: str):
    if gender == 'F':
        return 'female'
    elif gender == 'M':
        return 'male'


for i in range(0, 918):
    data['address'][0]['city'] = patients[i][5]
    data['address'][0]['country'] = patients[i][6]
    data['address'][0]['extension'][0]['extension'][0]['valueDecimal'] = match_country(patients[i][6])[0]
    data['address'][0]['extension'][0]['extension'][1]['valueDecimal'] = match_country(patients[i][6])[1]
    data['birthDate'] = str(datetime.now().year - int(patients[i][0][:2])) + patients[i][0][2:]
    data['extension'][1]['valueCode'] = patients[i][1]
    data['extension'][0]['extension'][0]['valueCoding']['display'] = patients[i][2].lower().capitalize()
    data['extension'][0]['extension'][1]['valueString'] = patients[i][2].lower().capitalize()
    data['extension'][2]['valueAddress']['city'] = patients[i][5]
    data['extension'][2]['valueAddress']['country'] = patients[i][6]
    data['name'][0]['family'] = patients[i][4].lower().capitalize()
    data['name'][0]['given'] = patients[i][3].lower().capitalize()
    data['telecom'][0]['value'] = str(random.randint(1000000000, 9999999998))
    data['gender'] = match_gender(patients[i][1])
    if match_gender(patients[i][1]) == 'male':
        data['identifier'][1]['value'] = "1" + str(random.randint(1000000000, 9999999998))
    elif match_gender(patients[i][1]) == 'female':
        data['identifier'][1]['value'] = "2" + str(random.randint(1000000000, 9999999998))
    data['extension'][2]['valueCode'] = match_gender(patients[i][1])
    data['address'][0]['postalCode'] = str(random.randint(10000, 99998))
    if random.randint(0, 1) == 0:
        data['maritalStatus']['text'] = 'Never Married'
        data['maritalStatus']['coding'][0]['display'] = 'Never Married'
        data['maritalStatus']['coding'][0]['code'] = 'S'
    else:
        data['maritalStatus']['text'] = 'Married'
        data['maritalStatus']['coding'][0]['display'] = 'Married'
        data['maritalStatus']['coding'][0]['code'] = 'M'

    rsp = requests.post("http://147.102.33.214:8080/fhir/Patient?_pretty=true", headers=Headers, data=json.dumps(data))
    if rsp.status_code == 400 or rsp.status_code == 404:
        print("Not Success!")
    elif rsp.status_code == 201:
        print("Success!")
    sleep(3)

# first patient id = 149953
# last patient id = 150871
