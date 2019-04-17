import random
import os

#Generate id for the person and increment the counter
file = open('id_index.txt','r')
id_person = int(file.readline())
file.close()
#if os.path.exists("id_index.txt"):
  #os.remove("id_index.txt")
file = open('id_index.txt','w')
id_person += 1
file.write(str(id_person))
file.close()

#Generate a random number and obtain the corresponding name in the names file
random_index_name = random.randint(1,100)
file = open('names.txt','r')
names = file.readlines()
name = names[random_index_name - 1].rstrip()
file.close()

#Generate a random age
random_age = random.randint(0,100)

#Sent Post request
#Payload is the json to be sent to the url
#payload = {}
#url is the url used for the requests
#url = ''
#r = requests.get('',json=payload)

#Debugging
print (id_person)
print (name)
print (random_age)