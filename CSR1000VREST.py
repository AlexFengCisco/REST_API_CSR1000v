'''
Test for REST api with CSR1000v
Python build 2.7.2+

Memo:
urlopen() must after Request(), and url and POST/PUT data must as
Request's input,

header input with Request instance .add_header(),
Header type depends on API request

as request method , if no data , default method is GET , if has data ,
method is POST
as for PUT and DELETE , has to input  get_method=lambada:'DELETE' or
'PUT' , Python urllib2 documentary has the detail

import urllib for encode data , bur failed , has to input data as string

for function , REST API is better than ONEpk API, cos java API has to
always kept the connection open ,
when connection closed , all application based routing information will
be deleted ,but REST API has no impact.

Tips:
Curl is better than Pycharm in debugging, cos http/https detail error
message only shown in Curl,
I think it was due to urllib2 only check the error code ,if not  
200>code<300 , response() will raise error

Date May 14 2014
@author: Alex Feng  alfeng@cisco.com
'''

import base64
import json
import urllib
import sys
from urllib2 import urlopen, Request, httplib
import paramiko



#constant

Url_type="https://"

Rest_host="192.168.255.133"

Rest_run_config="/api/v1/global/running-config"
Rest_sys_log="/api/v1/global/syslog"
Rest_Static_route="/api/v1/routing-svc/static-routes"
Rest_Routing_table="/api/v1/routing-svc/routing-table"
Rest_interfaces="/api/v1/interfaces/"

username="cisco"
password="cisco"

#creat user credential and get token id
print "test A point-----------"
credentials = base64.b64encode(username+":"+password)
headers = {'Authorization': 'Basic ' + credentials, 'Accept':
'application/json'}
response =urlopen(Request("https://192.168.255.133/api/v1/auth/token-services",b"",headers))
data = json.load(response)
token_id = data["token-id"]

print "token id ="+token_id

#get running config from router

url = "https://"+Rest_host+Rest_run_config

request=Request(url)
request.add_header('Accept','text/plain')
request.add_header('X-Auth-Token',token_id)
method=request.get_method()

response=urlopen(request)

text_content=response.read()

print text_content



#get sys log from router
'''
url = "https://"+Rest_host+Rest_sys_log

request=Request(url)
request.add_header('Accept','application/json')
request.add_header('X-Auth-Token',token_id)
method=request.get_method()
print method

response=urlopen(request)

json_content=json.load(response)


print json_content['messages']
'''

#post static route


url="https://"+Rest_host+Rest_Static_route

route1="50.50.50.50/32"
static_routes='{"destination-network":"'+route1+'","next-hop-router":"30.30.30.2","outgoing-interface":"GigabitEthernet1","admin-distance":3}'


#data=urllib.urlencode(static_route)

request=Request(url,static_routes)
request.add_header('Accept','application/json')
request.add_header('X-Auth-Token',token_id)
request.add_header('Content-type','application/json')

#headers =
{'Accept':'application/json','Content-type':'application/json','X-Auth-Token':token_id}
#response = urlopen(Request(url,static_route),headers)
#type=request.get_type()
#print type

response=urlopen(request)


#print json_content
print response.info()
print response.msg
print response.code
print response.geturl()


# get the route with rest API

'''
url="https://"+Rest_host+Rest_Routing_table

request=Request(url)
request.add_header('Accept','application/json')
request.add_header('X-Auth-Token',token_id)

response=urlopen(request)

json_content=json.load(response)
print json_content['items']

print response.geturl()
print response.msg
'''

#delete the route with rest API
'''
url="https://"+Rest_host+Rest_Static_route+"/42.40.40.40_32_30.30.30.1_GigabitEthernet1"

request=Request(url)
request.add_header('Accept','application/json')
request.add_header('X-Auth-Token',token_id)
request.get_method=lambda:'DELETE'
print request.get_method()

response=urlopen(request)
print response.info()
print response.code
print response.msg
'''

# put ip address and mask to interface

url=Url_type+Rest_host+Rest_interfaces+"Loopback1"
ip_add="6.6.6.6"
subnet_mask="255.255.255.0"


if_add_mask='{"type":"loopback","if-name":"Loopback1","ip-address":"'+ip_add+'","subnet-mask":"'+subnet_mask+'"}'
request=Request(url,if_add_mask)
request.add_header('Accept','application/json')
request.add_header('X-Auth-Token',token_id)
request.add_header('Content-type','application/json')
request.get_method=lambda:'PUT'

print request.get_method()

response=urlopen(request)
print response.code
print response.msg
print response.info()


#put interface status up and down

url=Url_type+Rest_host+Rest_interfaces+"Loopback1"+"/state"

if_state='{"if-name":"Loopback1","enabled":false}'
request=Request(url,if_state)
request.add_header('Accept','application/json')
request.add_header('X-Auth-Token',token_id)
request.add_header('Content-type','application/json')
request.get_method=lambda:'PUT'

print request.get_method()

response=urlopen(request)

print response.code
print response.msg
print response.info()



