import requests

headers = {'Content-type': 'application/json'}

# with open('observation-data.json', 'r') as json_in:
#     json_data = json_in.read()
#
# data = json.loads(json_data)
#
# for i in data['entry']:
#     i['resource']['effectiveDateTime'] = '2022-08' + i['resource']['effectiveDateTime'][7:]
#     i['resource']['issued'] = '2022-08' + i['resource']['effectiveDateTime'][7:]
#     rsp = requests.put(f'http://147.102.33.214:8080/fhir/Observation/{int(i["resource"]["id"])}?_format=json&_pretty=true', headers=headers, data=json.dumps(i['resource']))
#
#     if rsp.status_code == 200:
#         print('Success')
#     sleep(2)

rsp = requests.get('http://147.102.33.214:8080/fhir/Condition?_getpagesoffset=7&_count=1502&_pretty=true&_bundletype=searchset', headers=headers)
if rsp.status_code == 200:
    for i in rsp.json()['entry']:
        if i['resource']['recordedDate'][:7] != '2022-08':
            print('The date dose not match!')
