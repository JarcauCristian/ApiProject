import csv
import datetime
from pprint import pprint
from time import sleep
import requests
import json


def read_data():
    with open('heart_failure_clinical_records_dataset.csv', 'r') as csv_in:
        csv_reader = csv.reader(csv_in)
        data = []
        for row in csv_reader:
            data.append(row)
        data.pop(0)
    return data


def main():
    with open('request.json', 'r') as json_in:
        json_data = json_in.read()

    data = json.loads(json_data)
    hrt = read_data()
    headers = {"Content-Type": "application/json"}
    counter = 100271
    for i in range(0, 299):
        data['subject']['reference'] = f'Patient/{counter}'
        data['component'][0]['valueQuantity']['value'] = int(hrt[i][8])
        data['effectiveDateTime'] = str(datetime.datetime.now()).replace(" ", 'T').replace(".", "-04:00 ")[:25]
        data['issued'] = str(datetime.datetime.now()).replace(" ", 'T').replace(".", "-04:00 ")[:25]
        counter += 1
        rsp = requests.post("http://147.102.33.214:8080/fhir/Observation?_pretty=true", headers=headers, data=json.dumps(data))
        if rsp.status_code == 400 or rsp.status_code == 404:
            print("Not Success!")
        elif rsp.status_code == 201:
            print("Success!")
        sleep(3)


if __name__ == '__main__':
    main()
