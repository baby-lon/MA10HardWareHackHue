# -*- coding: utf-8 -*-
import httplib, urllib
import time
import serial
import json

from phue import Bridge

#_URL_ = "localhost:5000"
_URL_ = "elpisapi.net"
_POST_ = "/color/api/web"
#_POST_ = "/api/hw"
_COM_ = "/dev/tty.usbserial-A501KB7P"
#_COM_ = "/dev/tty.usbmodemfa131"
#_COM_ = "/dev/ttyUSB1"

#tmp_msg = _COM_ #"/dev/ttyUSB0"
#ser = serial.Serial(tmp_msg)
#ser.baudrate = 115200
#ser.timeout = 1
#print ser.portstr

service_name = "ThermoHygrometer"
hw_did = "0001"
state = "0"


postdata = {}
params = urllib.urlencode(postdata) 
headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
conn = httplib.HTTPConnection( _URL_,timeout=8 )
#try:
conn.request("GET", _POST_ , params, headers)
response = conn.getresponse()
data = response.read()
conn.close()
jdata = json.loads(data)

Roffset = int(jdata["red"] )
Goffset = int(jdata["green"] )
Boffset = int(jdata["blue"] )

b = Bridge('10.10.10.180')
b.connect()
b.get_api()

b.set_light(3, "bri", 0)
b.set_light(3, "hue", 0)

print 'init end'
		
while 1 :
	print 'loop'
	postdata = {}
	params = urllib.urlencode(postdata) 
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection( _URL_,timeout=8 )
	#try:
	conn.request("GET", _POST_ , params, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	jdata = json.loads(data)

	state = jdata["colorstr"]
	if state == "white":
		print state
		b.set_light(3, "bri", 200)
		b.set_light(3, "hue", 35000)
	elif state == "blue":
		print state
		b.set_light(3, "bri", 100)
		b.set_light(3, "hue", 24000)		
	elif state == "black":
		print state
		b.set_light(3, "bri", 50)
		b.set_light(3, "hue", 30000)
	elif state == "red":
		print state
		b.set_light(3, "bri", 50)
		b.set_light(3, "hue", 0)
	else:
		b.set_light(3, "bri", 0)
		b.set_light(3, "hue", 35000)

	
	time.sleep(1)
	

