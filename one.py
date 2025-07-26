import json

py_data = {
    "name": "Alice",
    "age": 30,
}
json_data = json.dumps(py_data)
print(json_data)

parsed_data = json.loads(json_data)
print(parsed_data)