import datetime
import threading
from time import sleep
from ShuffleData import shuffle
import requests
import json


def insert_data_obs(data, pos, hrt):
    headers = {"Content-Type": "application/json"}
    counter = 100271
    for i in range(0, 299):
        data['subject']['reference'] = f'Patient/{counter}'
        if pos == 3:
            data['valueQuantity']['value'] = float(hrt[i][pos])
        else:
            data['valueQuantity']['value'] = int(hrt[i][pos])
        data['effectiveDateTime'] = str(datetime.datetime.now()).replace(" ", 'T').replace(".", "-04:00 ")[:25]
        data['issued'] = str(datetime.datetime.now()).replace(" ", 'T').replace(".", "-04:00 ")[:25]
        counter += 1
        rsp = requests.post("http://147.102.33.214:8080/fhir/Observation?_pretty=true", headers=headers,
                            data=json.dumps(data))
        if rsp.status_code == 400 or rsp.status_code == 404:
            print("Not Success!")
        elif rsp.status_code == 201:
            print("Success!")
        sleep(2)
        counter += 1


def main():
    hrt = shuffle()
    # Read Anaemia Request
    with open('Anaemia.json', 'r') as json_in:
        anaemia_data = json_in.read()
    # Read CPK Request
    with open('Creatinine _Phosphokinase.json', 'r') as json_in:
        cpk_data = json_in.read()
    # Read Diabetes Request
    with open('Diabetes.json', 'r') as json_in:
        diabetes_data = json_in.read()
    # Read Ejection Fraction Request
    with open('Ejection_Fraction.json', 'r') as json_in:
        ejection_fraction_data = json_in.read()
    # Read Arterial Hypertension Request
    with open('Arterial_Hypertension.json', 'r') as json_in:
        arterial_hypertension_data = json_in.read()
    # Read Platelets Request
    with open('Platelets.json', 'r') as json_in:
        platelets_data = json_in.read()
    # Read Creatinine Request
    with open('Creatinine.json', 'r') as json_in:
        creatinine_data = json_in.read()
    # Read Sodium Request
    with open('Sodium.json', 'r') as json_in:
        sodium_data = json_in.read()
    # Read Smoker Request
    with open('Smoker.json', 'r') as json_in:
        smoker_data = json_in.read()
    # Read Date Death Request
    with open('Date_Death.json', 'r') as json_in:
        date_death_data = json_in.read()
    # Read Death Request
    with open('Death.json', 'r') as json_in:
        death_data = json_in.read()

    anaemia = json.loads(anaemia_data)
    cpk = json.loads(cpk_data)
    diabetes = json.loads(diabetes_data)
    ejection_fraction = json.loads(ejection_fraction_data)
    arterial_hypertension = json.loads(arterial_hypertension_data)
    platelets = json.loads(platelets_data)
    creatinine = json.loads(creatinine_data)
    sodium = json.loads(sodium_data)
    smoker = json.loads(smoker_data)
    date_death = json.loads(date_death_data)
    death = json.loads(death_data)

    observation_data = list()
    observation_data.append(cpk)
    observation_data.append(ejection_fraction)
    observation_data.append(platelets)
    observation_data.append(creatinine)
    observation_data.append(sodium)
    observation_data.append(date_death)

    condition_data = list()
    condition_data.append(anaemia)
    condition_data.append(diabetes)
    condition_data.append(arterial_hypertension)
    condition_data.append(smoker)
    condition_data.append(death)

    insert_data_obs_threads = list()
    pos = 0
    for observation in observation_data:
        insert_data_obs_thread = threading.Thread(target=insert_data_obs, args=(observation, pos, hrt))
        insert_data_obs_threads.append(insert_data_obs_thread)
        insert_data_obs_thread.start()
        pos += 1

    for thread in insert_data_obs_threads:
        thread.join()


if __name__ == '__main__':
    main()
