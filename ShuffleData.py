import random
import csv


def shuffle():
    with open('heart_failure_clinical_records_dataset.csv', 'r') as csv_in:
        csv_reader = csv.reader(csv_in)
        data = []
        for row in csv_reader:
            data.append(row)
        data.pop(0)
    random.shuffle(data)
    random.shuffle(data)
    random.shuffle(data)
    random.shuffle(data)
    return data

