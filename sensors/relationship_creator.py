import requests
import time
import random

relationship_list = ['Family','Work', 'Neighbor']
while(1):
    
    id1 = random.randint(0,1000)
    id2 = random.randint(0,1000)
    if id1 == id2:
        id2+=1

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
    time.sleep(2)