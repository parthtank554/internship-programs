# new code 
import requests
import json

URL = "http://127.0.0.1:8000/stuapi/"

def get_data(id=None): 
    headers = {'Content-Type': 'application/json'}
    if id is not None:
        data = json.dumps({'id': id})
        response = requests.post(URL, data=data, headers=headers)
    else:
        response = requests.get(URL)

    if response.status_code == 200:
        print("Response Data:", response.json())
    else:
        print("Error:", response.status_code, response.text)

# Example usage:
# get_data()         # Get all students
# get_data(1)        # Get student by ID = 1

# def post_data(name, roll, city):
#     headers = {'Content-Type': 'application/json'}
#     data = json.dumps({'name': name, 'roll': roll, 'city': city})
#     response = requests.post(URL, data=data, headers=headers)

#     if response.status_code == 201:
#         print("Student created successfully:", response.json())
#     else:
#         print("Error:", response.status_code, response.text)

def post_data():
    data = {
        'name': 'Vijay',
        'roll': 104,
        'city': 'Surat'
    }

    json_data = json.dumps(data)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL, data=json_data, headers=headers)
    data = response.json()
    print(data)
post_data()  # Call the function to post data  