import sys, optparse
import RPi.GPIO as GPIO
import time as time
from proton import *

GPIO.setmode (GPIO.BOARD)

GPIO.setup (22, GPIO.IN )
GPIO.setup (17,GPIO.OUT )
GPIO.setup (11, GPIO.OUT)

LED_STAT = False

def blinker (times):
    index = 0
    while (index < times):
        GPIO.output(11, True)
        sleep (1)
        GPIO.output(11,False)
        sleep (2)
        index = index + 1
    if (LED_STAT ==True)
        GPIO.output(11,True)



def main():
    print 'Welcome To ThermoMaster demo"
    blinker(3)
    print 'Hit the switch to get going"
    while True:
        if GPIO.input(22):
            break
    blinker(2)
    print "start"
    messenger = Messenger()
    message = Message()
    message.address = "amqps://owner:BFHk1n+EmRpTpbMtIH53zwcYxEpcDke/DLv1MOeKa1w=@thermomaster.servicebus.windows.net/statusupdt

    message.body = u"This is a text string"
    messenger.put(message)
    messenger.send()

    datafile = open ("tempreading.log","w")

    while True:
        GPIO.output (17, GPIO.HIGH)
        tfile = open ("/sys/bus/w1/devices/28-000005658920/w1_slave")
        text = tfile.read()
        tfile.close()
        secondline = text.split ("\n")[1]
        tempData = secondline.split(" ")[9]
        temprature = float (tempData[2:])
        temprature = temprature / 1000
        print temprature
        datafile.write(str(temprature)+ "\n")
        time.sleep (1)
        GPIO.output (17, GPIO.LOW)
        time. sleep (1)
        if GPIO.input (22)==1:
            break
    datafile.close()
    GPIO.output (17, GPIO.LOW)



if __name__ == '__main__':
  main()


