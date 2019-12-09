# This file should be run at Raspberry pi attached in buses
import blescan
import sys

import bluetooth._bluetooth as bluez

import math

from coapthon.client.helperclient import HelperClient
import spidev
import Adafruit_DHT
import time
import RPi.GPIO as gpio

from threading import Thread

import requests
import json

#humidity&temperature sensor
sensor=Adafruit_DHT.DHT11



#dust reading code
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 500000
LED = 21
gpio.setmode(gpio.BCM)
gpio.setup(LED, gpio.OUT)

servo_pin = 18	# PWM channel 0 pin 18(also can use GPIO 12 for PWM channel 0)
gpio.setup(servo_pin, gpio.OUT)
PWM_frequency = 50
servo_motor = gpio.PWM(servo_pin, PWM_frequency) 
servo_motor.start(0)	# Initial duty_cycle = 0. Duty cycle for servo motor can be varied between 3~7.5~12

host = "192.168.0.67"    #CoAP Server IP
port = 5683
path = "advanced"

client = HelperClient(server=(host, port))

host_lambda='https://cbqz37du17.execute-api.ap-northeast-2.amazonaws.com/default/ServoMotor'	#Host for lambda transaction to run servo motor

def dust_read(channel):	#calculate and send dust data here
	global calVoltage
	global dust_data

	gpio.output(LED, gpio.LOW)
	time.sleep(0.00028)
	adcValue = analog_read(channel)
	time.sleep(0.00004)
	gpio.output(LED,gpio.HIGH)
	time.sleep(0.00968)
	if calVoltage == 0.0:	# If it is first time of reading calVoltage
		calVoltage = adcValue*(3.3/1024)
        else:	# Else, save average value
        	calVoltage = (calVoltage + adcValue*(3.3/1024))/2
        dust_data = round((0.172 * calVoltage) * 1000, 6)
        print "dust_Data: %f" % (dust_data)

def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_out = ((r[1]&3) << 8) + r[2]
    return adc_out
    

#ble scanning code
dev_id = 0
try:
	sock = bluez.hci_open_dev(dev_id)
	print "ble thread started"

except:
	print "error accessing bluetooth device..."
    	sys.exit(1)

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

try:
	calVoltage = 0.0
	dust_data = 0.0
	while True:
		send_flag = 0	# To use for is it OK initialize dust_data and calVoltage value(flag 1 is OK for initialize)
                h,t=Adafruit_DHT.read_retry(sensor,14)
                if h is not None and t is not None:
                    print("Temperature ={0:0.1f}*C Humidity = {1:0.1f}%".format(t,h))
                else:
                    print("error")
                
		dust_read(0)
		time.sleep(1)
		returnedList = blescan.parse_events(sock, 10)
		lambda_data = {"dust_density": dust_data}
		rs_lambda = requests.post(host_lambda, json.dumps(lambda_data), headers=None)	# Get lambda transaction value for servo motor onoff
		print rs_lambda.json()
		lambda_dump = json.dumps(rs_lambda.json())
		lambda_list = json.loads(lambda_dump)
		print lambda_list[13]
		
		if lambda_list[13] == "1":
			#Set servo motor degree to +90
			servo_motor.ChangeDutyCycle(12)
		else:
			#Set servo motor degree to -90
			servo_motor.ChangeDutyCycle(3)
		print "----------"
		for beacon in returnedList:		
			tmpList = beacon.split(',')
			
			if int(tmpList[2]) == 2 and int(tmpList[3]) <= 3 and int(tmpList[3]) >= 1:	# tmpList[2] : Major, tmpList[3] : Minor
				if tmpList[5]>=-90:	# If TXpower is bigger than or equal -40# Send dust data to the server
					data_list = {'minor_num': tmpList[3], 'dust_density': dust_data}
					
					if h > 70: # If humidity is too high
                                            data_list['Unreliable'] = 'Too high humidity! Dust data value may be unreliable.'
                                            
                                        # Divise severity of fine dust density
                                        if dust_data > 250:
                                            data_list['Severity'] = 'VERY BAD'
                                        elif dust_data > 150:
                                            data_list['Severity'] = 'BAD'
                                        elif dust_data > 75:
                                            data_list['Severity'] = 'NORMAL'
                                        else:
                                            data_list['Severity'] = 'FINE'
                                            
					data_send = json.dumps(data_list)

					if send_flag == 1:	# Initialize calVoltage and dust_data for next measure section 
						calVoltage = 0.0
						dust_data = 0.0
					send_flag = 1	# Set send_flag 1 at bus station for initializing measured value

					print beacon
					response = client.put(path, data_send, timeout=5)	# Send CoAP server data
					print response.pretty_print()

				else :	# If TXpower is lower than -40 (if bus leave previous bus stop or not reach to next bus stop)
					send_flag = 0

except KeyboardInterrupt:
    print "Client Stop"
    client.stop()
    gpio.cleanup()
