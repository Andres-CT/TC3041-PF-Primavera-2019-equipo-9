import requests
import time
import random
import string

url = 'http://192.168.1.103:80/'
url_person = url+'person'
url_disease = url+'disease'
url_cure = url+'cure'
url_spread = url+'spread'

spread_list = ['Fluids', 'Touch', 'Air']

disease_name = input("Enter disease: ")
spread = input("Select spread method: 0 = Fluids, 1 = Touch, 2 = Air\n")
spread_rate_per_unit = input("Enter spread rate: ")
cure_rate_per_unit = input("Enter cure rate: ")
wait_time = input("Enter wait time(0 is valid): ")

#url_get = 'https://reqres.in/api/users/2'

get_people_response = requests.get(url_person).json()
people_count = get_people_response['count']
infected = random.randint(0,int(people_count))


payload = {'name':disease_name,'spread_type':spread,'infected_id':infected}
disease_creation_response = requests.post(url_disease,json=payload).json()
disease_id = disease_creation_response['id']
current_iteration = 1

while True:
    payload = {'id':disease_id}
    infected_number = requests.get(url_cure,json=payload).json()['count']
    if (infected_number == 0 | infected_number == people_count):
        break
    
    for i in range(spread_rate_per_unit):
        requests.post(url_spread, json=payload)
    
    for i in range(cure_rate_per_unit):
        requests.post(url_cure, json=payload)

    print("Finished iteration:", current_iteration)
    current_iteration += 1

    time.sleep(wait_time)

#string_idx = string_request.find("/"id/"")


#while(True):
 #   g = requests.get(url_cure. json)