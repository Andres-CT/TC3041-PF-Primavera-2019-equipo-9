import requests
import time
import random
import string

while(1):
    #url_get = 'http://192.168.1.65:80/disease'
    url_get = 'https://reqres.in/api/users/2'

    get_disease_request = requests.get(url_get)
    request_json = get_disease_request.json()
    request_string = str(request_json)
    request_string_idx = request_string.find("'id'")
    disease_count = request_string[request_string_idx + 8]

    id = random.randint(0, int(disease_count))
    payload = {'id':id}
    url = 'http://192.168.1.65:80/spread'
    r = requests.post()