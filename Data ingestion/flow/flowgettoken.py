# FLOW FROM SKY REST API
# Pedro Pimenta, Julho-Setembro 2022
# ppimenta@ipmaia.pt


# Necessary to profile this script
import time
start = time.perf_counter() # cpu time call at the beginning of the script

# Included to mark the beginning of the script in output 
print ("Flow ...")


import requests   # necessary to communicate over https with the REST APIs
import sys        # used for process communication - this script returns 0 if ended properly
# import json     # not necessary in this script, mentioned because it will be needed in next steps
# import datetime # not necessary in this script, mentioned because it will be needed in next steps

# yunex_flow_creds.py file contains the User credentials to access the Flow block (server-side)
# username="<user name>"
# userpass="<user password>"
import yunex_flow_creds


# url of the Flow block + port + end point
# host="https://89.180.211.96:8080/users/auth" # This script is being used just for one host at at time
# End points explained at https://flow-docs.readme.io/docs/basic-communication-with-flows-rest-api#authentication
host="https://93.102.140.115:8080/users/auth"

# definition of the headers
# check https://flow-docs.readme.io/docs/basic-communication-with-flows-rest-api#authentication 
# for further information about the parameters
headers = {
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer VTLMQILFQG',
    'Accept-Version': "1.14.0"
}

# this 'userID' is passed to the end point through a POST call, in the json property:
userId={
    "username": yunex_flow_creds.username,
    "password": yunex_flow_creds.userpass
}


ct1 = time.perf_counter() # time call before the request call

# Call to the end point - note the invocation of the 'request.post()' method.
req = requests.post(host, headers=headers, json=userId, verify=False)

# This request will raise the warning:
# C:\Python39\lib\site-packages\urllib3\connectionpool.py:1013: InsecureRequestWarning: Unverified HTTPS 
# request is being made to host '93.102.140.115'. Adding certificate verification is strongly advised.
# See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#ssl-warnings 

ct2 = time.perf_counter() # time call after the request call

# Received data:
print("Status", req.status_code)
print("Headers", req.headers)
print("Text",req.text)

# assuming we are just interested in the received token
#f = open("flowblocktoken.txt", "w")
#f.write(req.text)
#f.close()

# same results can be obtained by
open("flowblocktoken.txt", "w").write (req.text)


# At this point, the file "flowblocktoken.txt" contains the token (json format)
# we can use for subsequent calls
# Typical content of the flowblocktoken.txt file
# {"access_tokens":["<token>"]}

# The value of this token should be the same as the token shown in your Flow area, as mentioned in
# https://flow-docs.readme.io/docs/basic-communication-with-flows-rest-api#authentication 

ct3 = time.perf_counter() # time call after storing the received data

# Profiling this script

print ("request.post %5.3f secs; processing and storing answer %5.3f secs; overall %5.3f secs." % (ct2-ct1, ct3-ct2, ct3-start))

sys.exit(0)