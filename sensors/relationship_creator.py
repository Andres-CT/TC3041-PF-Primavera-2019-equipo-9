import requests
import time
import random
import json

relationship_list = ['FAMILY','WORK', 'NEIGHBOR']
while(1):
    url_get = 'http://192.168.1.65:80/person'
    #url_get = 'https://reqres.in/api/users/2'

    get_people_request = requests.get(url_get)
    request_json = get_people_request.json()
    request_string = str(request_json)
    request_string_idx = request_string.find("count")
    request_string_idx_end = request_string.find("}",int(request_string_idx))
    people_count = request_string[request_string_idx + 8:request_string_idx_end]

    id1 = random.randint(0, int(people_count))
    id2 = random.randint(0, int(people_count))
    if id1 == id2:
        if id1 == 0:
            id2=1
        else:
            id2-=1

    relatioship = relationship_list[random.randint(0,2)]
    #Sent Post request
    #payload is the json to be sent to the url
    payload = {'relation':relationship, 'first_id':id1, 'second_id':id2}
    #the url is the one used for the requests
    url = 'http://192.168.1.65:80/relationship'
    r = requests.post(url,json=payload)

    #Debugging
    print (relatioship)
    print (id1)
    print(id2)
    print(r.text)
    time.sleep(2)