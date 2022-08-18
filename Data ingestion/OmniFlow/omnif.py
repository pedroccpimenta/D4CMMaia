# Omniflow REST API
# OmniFlow
# Pedro Pimenta, Junho 2022


# Esta script deverá correr uma vez por dia e permitir obter
# uma token que expira em 24 horas.
# Essa token é armazenada no ficheiro omnitoken.txt
# e utilizada pela outra script que irá obter os valores
# de operação dos omniflows com maior periodicidade (1~2 hrs, p. exemplo)


import requests
import json
import sys
import datetime

print ("OmniFlow ...")

import requests

host="http://727a06227fcb.sn.mynetname.net:8081"

url = '/omniapi/oauth2/token?username=**UerName**&password=****PASSWORD****'
headers = {'Cache-Control': 
'no-cache','Content-Type': 'application/x-www-form-urlencoded,application/json',
'Host': '727a06227fcb.sn.mynetname.net:8081',
'Authorization': 'RequestOauth2'}

req = requests.get(host+url, headers=headers)

print(req.status_code)
print(req.headers)
print(req.text)
totok=req.json()
print (totok["token"])

ficheiro="/home/ppimenta/baze/opendatasoft/OmniFlow/omnitoken.txt"

f = open(ficheiro, "w")
f.write(totok["token"])
f.close()
