import datetime
import threading
from time import sleep
from ShuffleData import shuffle
import requests
import json


def insert_data_obs(data, pos, hrt):
    headers = {"Content-Type": "application/json"}
    counter = 100272
    for i in range(0, 149):
        data['subject']['reference'] = f'Patient/{counter}'
        if pos == 3:
            data['valueQuantity']['value'] = float(hrt[i][pos])
        else:
            data['valueQuantity']['value'] = int(hrt[i][pos])
        data['effectiveDateTime'] = str(datetime.datetime.now()).replace(" ", 'T').replace(".", "-04:00 ")[:25].replace("-09-13", "-09-11")
        data['issued'] = str(datetime.datetime.now()).replace(" ", 'T').replace(".", "-04:00 ")[:25].replace("-09-13", "-09-11")
        counter += 2
        rsp = requests.post("http://147.102.33.214:8080/fhir/Observation?_pretty=true", headers=headers,
                            data=json.dumps(data))
        if rsp.status_code == 400 or rsp.status_code == 404:
            print("Not Success!")
        elif rsp.status_code == 201:
            print("Success!")
        sleep(2)


def main():
    hrt = shuffle()
    # Read CPK Request
    with open('JSONFiles/Creatinine _Phosphokinase.json', 'r') as json_in:
        cpk_data = json_in.read()
    # Read Ejection Fraction Request
    with open('JSONFiles/Ejection_Fraction.json', 'r') as json_in:
        ejection_fraction_data = json_in.read()
    # Read Platelets Request
    with open('JSONFiles/Platelets.json', 'r') as json_in:
        platelets_data = json_in.read()
    # Read Creatinine Request
    with open('JSONFiles/Creatinine.json', 'r') as json_in:
        creatinine_data = json_in.read()
    # Read Sodium Request
    with open('JSONFiles/Sodium.json', 'r') as json_in:
        sodium_data = json_in.read()

    cpk = json.loads(cpk_data)
    ejection_fraction = json.loads(ejection_fraction_data)
    platelets = json.loads(platelets_data)
    creatinine = json.loads(creatinine_data)
    sodium = json.loads(sodium_data)

    observation_data = list()
    observation_data.append(cpk)
    observation_data.append(ejection_fraction)
    observation_data.append(platelets)
    observation_data.append(creatinine)
    observation_data.append(sodium)

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
