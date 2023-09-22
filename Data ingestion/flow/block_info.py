# FLOW FROM SKY
# Emanuel Ferreira, Julho-Outubro 2022
# emanuel.ferreira@cm-maia.pt

# IMPORTS
# -------------------------------------------------------------------------------------------------------------
import time
import requests   # necessary to communicate over https with the REST APIs
import sys        # used for process communication - this script returns 0 if ended properly
import json       # not necessary in this script, mentioned because it will be needed in next steps
import datetime   # not necessary in this script, mentioned because it will be needed in next steps
import flow_creds # flow_creds.py file contains the User credentials to access the Flow block (server-side)
                  # username = "<user name>"
                  # userpass = "<user password>"~
                  # access_token = "<user acess token retrieved in flow_gettoken.py>"
# -------------------------------------------------------------------------------------------------------------

# GET TIME SCRIPT START
start = time.perf_counter()

# SCRIPT START
print ("FLOW FROM SKY")

# URL TO GET BLOCK INFO
host_w = "https://93.102.140.115:8080/block_info"

# HEADERS
headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer oYoImLfHeIsQiHmXrYrQaKsAw',
    'Accept-Version': "1.14.0"
}

# USER CREDENDIALS -> flow_creds.py
userId = {
    "username": flow_creds.username,
    "password": flow_creds.userpass
}

# GET TIME BEFORE THE REQUEST CALL
ct1 = time.perf_counter() 

# GET CALL TO THE END POINT
req = requests.get(host_w, headers=headers, json=userId, verify=False)

# GET TIME AFTER THE REQUEST CALL
ct2 = time.perf_counter() 

# PRINT RESULTS
print("Status", req.status_code)
print("Headers", req.headers)
print("Text", req.text)

# WRITE RESULTS TO A .txt FILE
open(r"C:\Users\cmm1490\Documents\!MAIN\Projetos\Repositórios Git\Yunex-Data-Pipeline\Data export\block_info.txt", "w").write(req.text)

# GET TIME AFTER STORING THE RECEIVED DATA
ct3 = time.perf_counter()

# SCRIPT PROFILE
print ("Request.post %5.3f secs; Processing and storing answer %5.3f secs; Overall %5.3f secs." % (ct2-ct1, ct3-ct2, ct3-start))

sys.exit(0)