# Omniflow REST API
# OmniFlow
# Pedro Pimenta, Junho 2022

import config

import requests
import json
import sys
import datetime
import mysql.connector
from mysql.connector import Error

true=True 
false=False

#g='{"status":true,"light":0,"power":5,"baterry":93,"temperature":33,"wind":1}'
#b=json.loads(g)
#print("b:", b)
#print(b['status'])

#print (datetime.datetime.now())
#sys.exit(0)
print ("OmniFlow on ", sys.platform)
if sys.platform=="win32":
	ficheiro="omnitoken.txt"
else:		
	ficheiro="/home/ppimenta/baze/opendatasoft/OmniFlow/omnitoken.txt"


f = open(ficheiro, "r")
token = f.read()
f.close()
print ("token:", token)

host="http://727a06227fcb.sn.mynetname.net:8081"

idtocheck=[ "OL07210081", "OL07210082", "OL07210072"]
#idtocheck=["OL07210072"]
#idtocheck=["OL07210081"]
#idtocheck=["OL07210082"]

#for idc in idtocheck:
#	print (idc)
#
#exit (8)
persiste=True
#persiste=False


for idc in idtocheck:
	print ("ID2CK:", idc)
	getcmd = '/omniapi/v1/entities?omni_id='+idc
	headers = {'Cache-Control':'no-cache',
	'Content-Type': 'application/json',
	'Host': '727a06227fcb.sn.mynetname.net:8081',
	'x-auth-token':token}

	req = requests.get(host+getcmd, headers=headers)
	#b=req.status_code
	#print("b:",b)
	#print(req.headers)
	print ("OmniFlow id:", idc)
	print(req.text)
	b=json.loads(req.text)
	print("b:", b)
	agora=datetime.datetime.now()
	
	if 'baterry' in b:
		batte = str(b['baterry'])
	else:
		if "battery" in b:
			batte = str(b['baterry'])
		else:
			batte="null"

	if batte=="Not available":
		bbg="null"
	else:
		bbg=batte

	sql = "insert into OmniLeads (`datafile`, `OmniFlow_id`, status, light, power, temperature, wind, battery ) values ('"+agora.strftime("%Y-%m-%d %H:%M:%S")+"', '"+idc+"', '"+str(b['status'])+"', "+str(b['light'])+", "+str(b['power'])+", "+str(b['temperature'])+", "+str(b['wind'])+", "+bbg+");"
	#sql = "insert into OmniLeads (`datafile`, `OmniFlow_id`, status, light, power, temperature, wind ) values ('"+agora.strftime("%Y-%m-%d %H:%M:%S")+"', '"+idc+"', '"+str(b['status'])+"', "+str(b['light'])+", "+str(b['power'])+", "+str(b['temperature'])+", "+str(b['wind'])+");"
	print("sql:", sql)


	if persiste:
	    print("Para a Bdados:")
	    #print("r:",r)

	    try:
	        conn = mysql.connector.connect(
	                user=config.MariaUser,
	                password=config.MariaUpwd,
	                host="localhost",	               
	                port=3306,
	                database="BAZE")
	    
	    except Error as e:
	        print(f"Error connecting to MariaDB Platform: {e}")
	        sys.exit(-1)
	        
	    # Get Cursor
	    cur = conn.cursor()
	    cur.execute(sql)
	    conn.commit()
	    print(cur.rowcount)

	else:
	    print ("----- Valores não persistidos (persiste=",persiste,").")
	    sys.exit(1)


sys.exit(0)

#### Por vezes deixo algum código auxiliar 
getcmd = '/omniapi/v1/data/updateInstInfo?omni_id='+omniflow_id
req = requests.get(host+getcmd, headers=headers)

#print(req.status_code)
#print(req.headers)
#print ("OmniFlow id:", omniflow_id)
print(req.text)
