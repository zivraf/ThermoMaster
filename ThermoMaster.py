import sys, optparse
import RPi.GPIO as GPIO
import time as time
from proton import *

GPIO.setmode (GPIO.BOARD)

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
    if LED_STAT ==True:
        GPIO.output(11,True)



def main():
    print "Welcome To ThermoMaster demo"
    blinker(3)
    print "Hit the switch to get going"
    while True:
        if GPIO.input(15):
            break
    blinker(2)

    print "start"
    messenger = Messenger()
    message = Message()
    message.address = "amqps://owner:BFHk1n+EmRpTpbMtIH53zwcYxEpcDke/DLv1MOeKa1w=@thermomaster.servicebus.windows.net/statusupdt"

    message.body = u"This is a text string"
    messenger.put(message)
    messenger.send()

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
    print "-- temprature is " + temprature
    datafile.write(str(temprature)+ "\n")
    time.sleep (1)
    GPIO.output (7, GPIO.LOW)
    time. sleep (1)
   
    datafile.close()
    print "--Leaving Main"



if __name__ == '__main__':
  main()


