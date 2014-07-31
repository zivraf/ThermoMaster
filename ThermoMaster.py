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

def blinker (times):
    index = 0
    print "--Blinker ", times, " times"
    while (index < times):
        print "--Blink ", index+1
        GPIO.output(11, True)
        time.sleep (1)
        GPIO.output(11,False)
        time.sleep (1)
        index = index + 1
    if LED_STAT == True:
        GPIO.output(11,True)


def main():
    print "Welcome To ThermoMaster demo"
    blinker(3)
    print "Hit the switch to get going"
    while True:
        buttonIn = not GPIO.input(15)
        if buttonIn:
            break
        
    blinker(2)

    print "start"
    messenger = Messenger()
    message = Message()
    message.address = "amqps://owner:BFHk1n+EmRpTpbMtIH53zwcYxEpcDke/DLv1MOeKa1w=@thermomaster.servicebus.windows.net/statusupdt"

    datafile = open ("tempreading.log","w")

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


    message.body = "ThermoMaster 1.0 - Status Update"
    message.properties = dict()
    #message.subject = u"ThermoMaster Status Update"
    #message.properties [u"UpdateTime"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #message.properties [u"DeviceId"] = "28-000005658920"
    #message.properties [u"Temprature"] = temprature
    
    print "-- Message properties ", message.properties

    messenger.put(message)
    messenger.send()

    print "-- Message sent"

 
    time.sleep (1)
    GPIO.output (7, GPIO.LOW)
   
    datafile.close()
    print "--Leaving Main"



if __name__ == '__main__':
  main()


