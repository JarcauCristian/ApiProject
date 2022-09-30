import csv
from pprint import pprint

with open('patients.csv', 'r') as csv_in:
    csv_data = csv.reader(csv_in)

    patients = list()
    for row in csv_data:
        patients.append(row)

patients.pop(0)

with open('heart.csv', 'r') as csv_in:
    csv_data = csv.reader(csv_in)

    hrt = list()
    for row in csv_data:
        hrt.append(row)

hrt.pop(0)

counter = 0
for i in range(301, 1219):
    patients[i][0] = str(hrt[counter][0]) + patients[i][0][4:]
    patients[i][1] = hrt[counter][1]
    counter += 1

with open('patients_2.csv', 'w', newline='') as csv_out:
    csv_writer = csv.writer(csv_out)
    csv_writer.writerows([patients[i] for i in range(301, 1219)])
