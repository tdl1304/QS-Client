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
    'Host': 'qs.stud.iie.ntnu.no',
    'Origin': 'https://qs.stud.iie.ntnu.no',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Referer': 'https://qs.stud.iie.ntnu.no/student',
    'Accept-Language': 'nb-NO,nb;q=0.8,no;q=0.6,nn;q=0.4,en-US;q=0.2,en;q=0.2,da;q=0.2'
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

res = req(actions['login']['url'], {"email": username, "password": passwd}, header, actions['login']['method'])
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
    time.sleep(3)
print("Queue open")
queue_id = req(actionUrl=actions['addToQueue']['url'],
               data={"subjectID": subject_id, "roomID": room_id, "desk": desk_id, "message": message, "help": help,
                     "exercises": tasks},
               headers=header,
               method=actions['addToQueue']['method'])["queueElementID"]
print("Added to queue", queue_id)
