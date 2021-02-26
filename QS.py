import requests
import time
import json
from pathlib import Path

actions = {
    'studentSubjects': {'method': 'POST', 'url': 'res/studentSubjects'},
    'login': {'method': 'POST', 'url': 'loginForm'},
    'addToQueue': {'method': 'POST', 'url': 'res/addQueueElement'},
    'postpone': {'method': 'POST', 'url': 'res/studentPostponeQueueElement'},
    'getQueue': {'method': 'POST', 'url': 'res/getQueue'},
    'room': {'method': 'GET', 'url': 'res/room'}
}

header = {
    'Content-Type': 'application/json'
}

qs_api = 'https://qs.stud.iie.ntnu.no/'


def req(actionUrl, data, headers, method):
    if method == 'POST':
        return requests.post(qs_api + actionUrl, data=data, headers=headers)
    elif method == 'GET':
        return requests.get(qs_api + actionUrl, data=data, headers=headers)
    else:
        return None


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

res = requests.post(url="https://qs.stud.iie.ntnu.no/loginForm", headers=header, data=
"{\r\n    \"email\":\""+username+"\",\r\n    \"password\":\""+passwd+"\"\r\n}\r\n\r\n")
if res.status_code != 200:
    print('Password and username is wrong, change or delete login file')
    input('Press exit to end program')
    exit(0)
header['Cookie'] = res.headers["Set-Cookie"]

for element in req(actions['studentSubjects']['url'], None, header, actions['studentSubjects']['method']).json():
    if element['subjectActive'] != 0:
        print("Id:", element['subjectID'], element['subjectCode'], element['subjectName'],
              "(Active)" if element['subjectQueueStatus'] == 1 else "")

subject_id = int(input('Enter subject ID: '))

rooms = req(actions['room']['url'], None, header, actions['room']['method']).json()

for element in rooms:
    print("Id:", element['roomID'], element['roomNumber'])

room_id = int(input('Enter room ID: '))
desk_id = int(input('Enter desk ID: '))

tasks = []
i = -1

print("Add tasks (0 to exit)")
while i != 0 or tasks.__len__() == 0:
    i = int(input("Add task: "))
    if i != 0:
        tasks.append(i)
        print("Tasks: ", tasks)

subjectQueueStatus = 0

help = False
if input("Help? (y/n)") == "y":
    help = True

message = input("Message:")

print("Waiting for queue")

while subjectQueueStatus == 0:
    for element in req(actions['studentSubjects']['url'], None, header, actions['studentSubjects']['method']).json():
        if element['subjectID'] == subject_id:
            subjectQueueStatus = element['subjectQueueStatus']
            if subjectQueueStatus != 0:
                break
    time.sleep(2)
print("Queue open")

payload = "{\r\n    \"subjectID\":\""+str(subject_id)+"\",\r\n    \"roomID\":\""+str(room_id)+"\",\r\n    \"desk\":\""+str(desk_id)+"\",\r\n    \"message\":\""+message+"\",\r\n    \"help\":"+str(help).lower()+",\r\n    \"exercises\":"+str(tasks)+"\r\n}"
send = True
while send:
    response = requests.request("POST", "https://qs.stud.iie.ntnu.no/res/addQueueElement", headers=header, data=payload)
    if response.status_code == 200:
        send = False
print("Added to queue", response.json()['queueElementID'])
input('Press anything to exit')
