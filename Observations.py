import csv
import datetime
import threading
from time import sleep
import requests
import json


def insert_data_obs(data, pos, hrt):
    headers = {"Content-Type": "application/json"}
    counter = 149953
    for i in range(0, 918):
        data['subject']['reference'] = f'Patient/{counter}'
        # if pos == 7:
        #     data['valueQuantity']['value'] = float(hrt[i][pos])
        # else:
        data['valueQuantity']['value'] = int(hrt[i][pos])
        data['effectiveDateTime'] = str(datetime.datetime.now()).replace(" ", 'T').replace(".", "-04:00 ")[:25].replace("-09-13", "-09-11")
        data['issued'] = str(datetime.datetime.now()).replace(" ", 'T').replace(".", "-04:00 ")[:25].replace("-09-13", "-09-11")
        counter += 1
        rsp = requests.post("http://147.102.33.214:8080/fhir/Observation?_pretty=true", headers=headers,
                            data=json.dumps(data))
        if rsp.status_code == 400 or rsp.status_code == 404:
            print("Not Success!")
        elif rsp.status_code == 201:
            print("Success!")
        sleep(2)


def main():

    with open('heart.csv', 'r') as csv_in:
        csv_data = csv.reader(csv_in)
        data = []
        for row in csv_data:
            data.append(row)
        data.pop(0)

    hrt = []
    for i in data:
        i.pop(0)
        i.pop(0)
        hrt.append(i)

    # Read Chest Pain Type Request
    with open('JSONFiles/Chest_Pain_Type.json', 'r') as json_in:
        cpt_data = json_in.read()
    # Read Blood Pressure Request
    with open('JSONFiles/BloodPressure.json', 'r') as json_in:
        bp_data = json_in.read()
    # Read Cholesterol Request
    with open('JSONFiles/Cholesterol.json', 'r') as json_in:
        cholesterol_data = json_in.read()
    # Read Blood Sugar Request
    with open('JSONFiles/BloodSugar.json', 'r') as json_in:
        bs_data = json_in.read()
    # Read ECG Request
    with open('JSONFiles/ECG.json', 'r') as json_in:
        ecg_data = json_in.read()
    # Read Heart Rate Request
    with open('JSONFiles/HeartRate.json', 'r') as json_in:
        htr_data = json_in.read()
    # Read Angina Request
    with open('JSONFiles/Angina.json', 'r') as json_in:
        angina_data = json_in.read()
    # Read ST Request
    with open('JSONFiles/Old-Peak.json', 'r') as json_in:
        st_data = json_in.read()
    # Read ST Slope Request
    with open('JSONFiles/ST_Slope.json', 'r') as json_in:
        st_slope_data = json_in.read()
    # Read Heart Disease Request
    with open('JSONFiles/Heart_Disease.json', 'r') as json_in:
        hrt_disease_data = json_in.read()

    cpt = json.loads(cpt_data)
    bp = json.loads(bp_data)
    cholesterol = json.loads(cholesterol_data)
    bs = json.loads(bs_data)
    ecg = json.loads(ecg_data)
    htr = json.loads(htr_data)
    angina = json.loads(angina_data)
    st = json.loads(st_data)
    st_slope = json.loads(st_slope_data)
    hrt_disease = json.loads(hrt_disease_data)

    observation_data = list()
    observation_data.append(cpt)
    observation_data.append(bp)
    observation_data.append(cholesterol)
    observation_data.append(bs)
    observation_data.append(ecg)
    observation_data.append(htr)
    observation_data.append(angina)
    observation_data.append(st)
    observation_data.append(st_slope)
    observation_data.append(hrt_disease)

    # insert_data_obs_threads = list()
    # pos = 0
    # for observation in observation_data:
    #     insert_data_obs_thread = threading.Thread(target=insert_data_obs, args=(observation, pos, hrt[]))
    #     insert_data_obs_threads.append(insert_data_obs_thread)
    #     insert_data_obs_thread.start()
    #     pos += 1
    #
    # for thread in insert_data_obs_threads:
    #     thread.join()

    insert_data_obs(bs, 3, hrt)


if __name__ == '__main__':
    main()

# 0 ATA 1 TA 2 NAP 3 ASY
# 0 Normal 1 ST 2 LVH
# 0 Down 1 Flat 2 Up
