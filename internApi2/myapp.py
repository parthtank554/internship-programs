# import requests
# import json

# URL = "http://127.0.0.1:8000/studcreate/"
# data = {
#     "name": "John Doe",
#     "roll": 123,
#     "city": "New York"
# }

# json_data = json.dumps(data)
# r = requests.post(url=URL, data=json_data)
# r = requests.post(url=URL, data=json_data, headers={'Content-Type': 'application/json'})


# data = r.json()
# print(data)


import requests
import json

URL = "http://127.0.0.1:8000/studcreate/"

data = {
    'name': 'Parth',
    'roll': 101,
    'city': 'Junagadh'
}

json_data = json.dumps(data)
headers = {'Content-Type': 'application/json'}

response = requests.post(url=URL, data=json_data, headers=headers)

print("Status:", response.status_code)
print("Response:", response.json())
