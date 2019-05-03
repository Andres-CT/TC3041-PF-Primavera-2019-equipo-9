import requests
import time
import random
import json

url_get = 'http://192.168.1.103:80/person'
relationship_list = ['FAMILY','WORK', 'NEIGHBOR']
get_people_request = requests.get(url_get)
people_count = get_people_request.json()['count']
for it in range(30000):
    #url_get = 'https://reqres.in/api/users/2'

    id1 = random.randint(0, int(people_count))
    id2 = random.randint(0, int(people_count))
    if id1 == id2:
        if id1 == 0:
            id2=1
        else:
            id2-=1

    relationship = relationship_list[random.randint(0,2)]
    #Sent Post request
    #payload is the json to be sent to the url
    payload = {'relation':relationship, 'first_id':id1, 'second_id':id2}
    #the url is the one used for the requests
    url = 'http://192.168.1.103:80/relation'
    r = requests.post(url,json=payload)

    #Debugging
    #print (relationship)
    #print (id1)
    #print(id2)
    #print(r.text)
    #time.sleep(2)