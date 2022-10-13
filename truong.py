#by: NGO QUANG TRUONG
#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import datetime
import serial
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
port = serial.Serial("/dev/ttyAMA0", baudrate = 9600, timeout = 5)

port.write("AT+CMGF=1\r")                       # set to text mode
time.sleep(3)
port.write('AT+CMGDA="DEL ALL"\r')              # delete all SMS
time.sleep(3)
reply = port.read(port.inWaiting())             # Clean buf
print "Waiting for incomming SMS..."
def GPS():
    port.write('AT'+'\r\n')                     # AT Command
    data = port.read(1000)
    print data
    time.sleep(.5)
    port.write('AT+CGPSPWR=1'+'\r\n')           # Turn on GPS
    data = port.read(1000)
    print data
    time.sleep(.5)
    port.write('AT+CGPSRST=0'+'\r\n')           # Reset in Cold start mode
    data = port.read(1000)
    print data
    time.sleep(.5)
    port.write('AT+CGPSINF=0'+'\r\n')           # GPS info
    data = port.read(1000)
    print data
    time.sleep(.5)
    port.write('AT+CGPSSTATUS?'+'\r\n')         # Fix GPS
    data = port.read(1000)
    print data
    time.sleep(.5)
    port.write('AT+CGPSSTATUS?'+'\r\n')         # Fix GPS
    data = port.read(1000)
    print data
    time.sleep(.5)
    port.write('AT+CGNSPWR=1'+'\r\n')           # Power on the GNSS
    data = port.read(1000)
    print data
    time.sleep(.5)
    port.write('AT+CGNSSEQ="RMC"'+'\r\n')       # NMEA sentence
    data = port.read(1000)
    print data
    time.sleep(1.5)
    port.write('AT+CGNSINF'+'\r\n')             # Get GPS info
    data = port.read(1000)
    print data
    time.sleep(3)
    print "https://maps.google.com/maps?q=loc:", data[46:55], data[56:66]
    time.sleep(4)
    return "\nhttps://maps.google.com/maps?q=" + data[46:55] + "," + data[56:66]
while True:
    reply = port.read(port.inWaiting())
    if reply != "":                                  
        port.write("AT+CMGR=1\r") 
        time.sleep(3)
        reply = port.read(port.inWaiting())
        print reply                                  # in noi dung tin nhan
        if "Vitri" in reply:                         # tin nhan la "Vitri"
            Vitri = GPS()
            t = str(datetime.datetime.now())
            print "\nGoi dien\n"
            port.write('ATD+84888677000;\r\n')
            time.sleep(20)
            port.write('ATH\r\n')
            time.sleep(5)
            print "Dang gui vi tri toi sdt\r\n"
            port.write('AT+CMGS="+84888677000"\r')   # thiet lap nhan tin toi sdt
            time.sleep(3)
            msg = Vitri
            print t + "\nVitri: " + msg
            port.write(t + msg + chr(26))            # chr(26): \x1A hoac Ctrl+Z
        time.sleep(3)
        port.write('AT+CMGDA="DEL ALL"\r')           # delete all
        time.sleep(3)
        port.read(port.inWaiting())                  # Clear buf
    time.sleep(5)
GPIO.cleanup()      
