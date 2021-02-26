import json
from pathlib import Path

import requests
import time as time

url = "https://qs.stud.iie.ntnu.no/res/deleteQueueElement"

payloadQueue = "{\"subjectID\":\"185\"}"
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'
}
whitelist = [11068, 11060]
if Path("qs.psw").is_file():
    with open('qs.psw') as data_file:
        data_loaded = json.load(data_file)
        username = data_loaded["email"]
        passwd = data_loaded["password"]
    print("Username and password loaded from qs.psw")
else:
    username = input("Username: ")
    passwd = input("Password: ")
    if input("Do you want to save the username and password? WARNING SAVED IN CLEAR TEXT!  (y/n)") == "y":
        with open('qs.psw', 'w') as outfile:
            json.dump({"email": username, "password": passwd}, outfile)
    print("Username and passwd saved to qs.psw")

res = requests.post(url="https://qs.stud.iie.ntnu.no/loginForm", headers=headers, data=
"{\r\n    \"email\":\""+username+"\",\r\n    \"password\":\""+passwd+"\"\r\n}\r\n\r\n")
if res.status_code != 200:
    print('Password and username is wrong, change or delete login file')
    input('Press exit to end program')
    exit(0)
headers['Cookie'] = res.headers["Set-Cookie"]

while True:
    queue = requests.request("POST", "https://qs.stud.iie.ntnu.no/res/getQueue", headers=headers, data=payloadQueue)
    not_prioritized = [element for element in queue.json() if not element['subjectPersonID'] in whitelist]
    for student in not_prioritized:
        payload = "{\"queueElementID\": \"" + str(student['queueElementID']) + "\", \"subjectID\": \"185\"}"
        response = requests.request("POST", url, headers=headers, data=payload)
        print('deleted student:', student['personFirstName'], student['personLastName'])
    time.sleep(10)
    print("Trying to delete")
