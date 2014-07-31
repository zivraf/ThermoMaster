import sys, optparse
import RPi.GPIO as GPIO
import time as time
import datetime
from time import gmtime, strftime
from proton import *

GPIO.setmode (GPIO.BOARD)
GPIO.cleanup()

GPIO.setup (15, GPIO.IN )
GPIO.setup (7, GPIO.OUT )
GPIO.setup (11, GPIO.OUT)

LED_STAT = False
LED_PIN = 11
BUTTON_PIN = 15
SENSOR_PIN = 7

AMQP_CONN_STR = "amqps://owner:BFHk1n+EmRpTpbMtIH53zwcYxEpcDke/DLv1MOeKa1w=@thermomaster.servicebus.windows.net/statusupdt"

def blinker (times):
    index = 0
    print "--Blinker ", times, " times"
    while (index < times):
        print "--Blink ", index+1
        GPIO.output(11, True)
        time.sleep (.2)
        GPIO.output(11,False)
        time.sleep (.2)
        index = index + 1
    if LED_STAT == True:
        GPIO.output(11,True)

def buttonCallBack (channel):
    print "--callback"
    if LED_STAT:
        print "--turn off"
        LED_STAT = False
    else:
        print "--turn on"
        LED_STAT = True    
    GPIO.output (LED_PIN,LED_STAT)

def sendMessage (oper, value):
    message = Message()
    message.address = AMQP_CONN_STR
    message.body = u"ThermoMaster 1.0 - Status Update"
    prop = {}
    prop [u"DeviceId"] = u"28-000005658920"
    currTime =  time.asctime( time.localtime(time.time()) )
    prop [u"UpdtTime"] = currTime
    prop [u"cmd"] = oper
    prop [u"value"] = value
    message.properties = prop
    messenger.put(message)
    messenger.send()

def main():
    print "Welcome To ThermoMaster demo"
    blinker(3)
    print "Hit the switch to get going"
    while True:
        buttonIn = GPIO.input(15)
        if buttonIn:
            break
        
    blinker(2)

    GPIO.add_event_detect (BUTTON_PIN, GPIO.RISING, callback= buttonCallBack, councetime=500)
    print "start"
    messenger = Messenger()
    message = Message()
    message.address = "amqps://owner:BFHk1n+EmRpTpbMtIH53zwcYxEpcDke/DLv1MOeKa1w=@thermomaster.servicebus.windows.net/statusupdt"

    datafile = open ("tempreading.log","w")

    while True:

        print "--reading temprature"

        GPIO.output (7, GPIO.HIGH)
        tfile = open ("/sys/bus/w1/devices/28-000005658920/w1_slave")
        text = tfile.read()
        tfile.close()
        print "-- closed dev file"
        secondline = text.split ("\n")[1]
        tempData = secondline.split(" ")[9]
        temprature = float (tempData[2:])
        temprature = temprature / 1000
        print "-- temprature is " , temprature
        datafile.write(str(temprature)+ "\n")


        message.body = u"ThermoMaster 1.0 - Status Update"
        prop = {}
        prop [u"DeviceId"] = u"28-000005658920"
        currTime =  time.asctime( time.localtime(time.time()) )
        prop [u"UpdtTime"] = currTime
        prop [u"Temprature"] = temprature

        message.properties = prop
        #message.subject = u"ThermoMaster Status Update"
        #message.properties [u"UpdateTime"] = currTime
        #message.properties [u"DeviceId"] = "28-000005658920"
        #message.properties [u"Temprature"] = temprature
        
        print "-- Message properties ", message.properties

        messenger.put(message)
        messenger.send()

        print "-- Message sent"

     
        time.sleep (1)
        GPIO.output (7, GPIO.LOW)

        time.sleep (10)
   
    datafile.close()
    print "--Leaving Main"



if __name__ == '__main__':
  main()


