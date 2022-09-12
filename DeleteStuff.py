import requests
from pprint import pprint
import pandas as pd
import json
fhirURL = 'http://147.102.33.214:8080/fhir/Patient?_id=100381&_revinclude=Observation:subject&_revinclude=Condition:subject'
rsp = requests.get(fhirURL)
cdf = pd.json_normalize(rsp.json()).explode('entry')
json_struct = json.loads(cdf.to_json(orient="records"))
df_flat = pd.json_normalize(json_struct)
pprint(df_flat)
