from pprint import pprint

import requests

for i in range(100272, 100570, 2):
    rsp = requests.get(f'http://147.102.33.214:8080/fhir/Patient?_id={i}&_revinclude=Observation:subject&_revinclude=Condition:subject&_pretty=True')
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

    pprint(CPK)

