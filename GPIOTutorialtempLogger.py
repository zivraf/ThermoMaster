import RPi.GPIO as GPIO
import time as time
GPIO.setmode (GPIO.BCM)
GPIO.setup (22, GPIO.IN )
GPIO.setup (17,GPIO.OUT )

while True:
    if GPIO.input(22):
        break

print "start"

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
