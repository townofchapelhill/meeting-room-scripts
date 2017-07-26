import requests
import json

j = open('patronsv1.json', 'r')

lines = j.readlines()

j.close()

n = open('patronsv1.json', 'w')

for line in lines:
    if line == ']}':
        continue
    n.write(line)

n.write(',')

url = "https://catalog.chapelhillpubliclibrary.org/iii/sierra-api/v3/token"
header = {"Authorization": "Basic NVZuT3lhZXltczdUWUFsWnJnVDQrV0MyK2ZaUDpyRjBpaUBDVyF0bThMTGw4", "Content-Type": "application/x-www-form-urlencoded"}
response = requests.post(url, headers=header)
json_response = json.loads(response.text)
token = json_response["accesse_token"]





