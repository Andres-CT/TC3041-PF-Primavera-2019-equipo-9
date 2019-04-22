import requests
import time
import random
import string

disease_id = -1
spread_list = ['Fluids', 'Touch', 'Air']
while(1):
    disease_id += 1
    disease_name = ''.join([random.choice(string.ascii_lowercase) for n in xrange(5)])
    spread = spread_list[random.randint(0,2)]
    infected = random.randint(0,1000)


    payload = {'id':disease_id, 'name':disease_name,'spread_type':spread,'infected_id':infected}
    url = 'http://192.168.1.65:80/disease'
    r = requests.post(url,json=payload)

    #Debugging
    print(disease_id)
    print(disease_name)
    print(spread)
    print(infected)

    time.sleep(2)