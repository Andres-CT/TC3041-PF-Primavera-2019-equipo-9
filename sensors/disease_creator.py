import requests
import time
import random
import string


spread_list = ['Fluids', 'Touch', 'Air']
while(1):
    disease_name = ''.join([random.choice(string.ascii_lowercase) for n in xrange(5)])
    spread = spread_list[random.randint(0,2)]
    url_get = 'http://192.168.1.65:80/person'
    #url_get = 'https://reqres.in/api/users/2'

    get_people_request = requests.get(url_get)
    request_json = get_people_request.json()
    request_string = str(request_json)
    request_string_idx = request_string.find("count")
    request_string_idx_end = request_string.find("}",int(request_string_idx))
    people_count = request_string[request_string_idx + 8:request_string_idx_end]
    infected = random.randint(0,int(people_count))


    payload = {'name':disease_name,'spread_type':spread,'infected_id':infected}
    url = 'http://192.168.1.65:80/disease'
    r = requests.post(url,json=payload)

    #Debugging
    print(disease_id)
    print(disease_name)
    print(spread)
    print(infected)
    print(r.text)

    time.sleep(2)