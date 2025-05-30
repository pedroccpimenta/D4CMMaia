# FLOW FROM SKY
# Emanuel Ferreira, Julho-Outubro 2022
# emanuel.ferreira@cm-maia.pt

# IMPORTS
# -------------------------------------------------------------------------------------------------------------
import time       # necessary to define the timestamps to ISO8601
import requests   # necessary to communicate over https with the REST APIs
import sys        # used for process communication - this script returns 0 if ended properly
import json       # not necessary in this script, mentioned because it will be needed in next steps
import datetime   # not necessary in this script, mentioned because it will be needed in next steps
import flow_creds # flow_creds.py file contains the User credentials to access the Flow block (server-side)
                  # username = "<user name>"
                  # userpass = "<user password>"~
                  # access_token = "<user acess token retrieved in flow_gettoken.py>"
import pprint as pp
# -------------------------------------------------------------------------------------------------------------

# GET TIME SCRIPT START
start = time.perf_counter()

# SCRIPT START
print ("FLOW FROM SKY")

# URL TO GET SINKS HISTORY
host_w = "https://93.102.140.115:8080/cubes/0/analytics/0/sinks/history"

# HEADERS
headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer oYoImLfHeIsQiHmXrYrQaKsAw',
    'Accept-Version': "1.14.0"
}

# TIMESTAMP FORMAT
timestamp_format = datetime.datetime.now().isoformat()

# USER CREDENDIALS -> flow_creds.py
userId = {
    "username": flow_creds.username,
    "password": flow_creds.userpass
}

sinkhist = {  
    "sequence_number": "144",  
    "sinks":     
        {      
            "id": 0  
        }
}

# GET TIME BEFORE THE REQUEST CALL
ct1 = time.perf_counter()

# GET CALL TO THE END POINT
req = requests.post(host_w, headers=headers, json=sinkhist, verify=False)

# GET TIME AFTER THE REQUEST CALL
ct2 = time.perf_counter() 

# PRINT RESULTS
print("Status", req.status_code)
print("Headers", req.headers)
print("Text", req.text)

# WRITE RESULTS TO A .txt FILE
open(r"C:\Users\cmm1490\Documents\!MAIN\Projetos\Repositórios Git\Yunex-Data-Pipeline\Data export\sinks_hist.txt", "w").write(req.text)

# GET TIME AFTER STORING THE RECEIVED DATA
ct3 = time.perf_counter()

# SCRIPT PROFILE
print ("Request.post %5.3f secs; Processing and storing answer %5.3f secs; Overall %5.3f secs." % (ct2-ct1, ct3-ct2, ct3-start))

sys.exit(0)