# -*- coding: utf-8 -*-
from mq import *
from sys import stderr
from threading import Lock
import sys, time, os, traceback, thread
import RPi.GPIO as GPIO    
from re import findall
from subprocess import check_output   

pin14 = 14
pin15 = 15                    # Пин отвечающий за управление
pinState = False
dopPinState = False  

myCmd0 = 'echo 130 | nc -w1 -u -b 192.168.5.255 11111'
myCmd1 = 'echo 131 | nc -w1 -u -b 192.168.5.255 11111'
myCmd2 = 'echo 132 | nc -w1 -u -b 192.168.5.255 11111'
myCmd3 = 'echo 133 | nc -w1 -u -b 192.168.5.255 11111'   
def myFunc():
    while True:
	os.system("echo 20" + str(mq4.val["LPG4"]) + " ppm | nc -w1 -u -b 192.168.5.255 11111")
	os.system("echo 21" + str(mq5.val["LPG5"]) + " ppm | nc -w1 -u -b 192.168.5.255 11111")
	time.sleep(2)

def signal14(pin):
	os.system(myCmd0)
	return
def signal15(pin):
	os.system(myCmd1)
	return
try:
    lock = Lock()
    print("Press CTRL+C to abort.")	    
    mq4 = MQ(10, 0, 4)
    os.system('echo Калибровка 1/4 пройдена | nc -w1 -u -b 192.168.5.255 11111')
    mq5 = MQ(10, 1, 5)
    os.system('echo Калибровка 2/4 пройдена | nc -w1 -u -b 192.168.5.255 11111')
   # mq6 = MQ(10, 2, 6)
    #os.system('echo Калибровка 3/4 пройдена | nc -w1 -u -b 192.168.5.255 11111')
    #mq9 = MQ(10, 3, 9)
    os.system('echo Уровень газа в норме | nc -w1 -u -b 192.168.5.255 11111')
    
    GPIO.setmode(GPIO.BCM)                 
    GPIO.setup(pin14, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(pin15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    
    GPIO.add_event_detect(pin14, GPIO.RISING)
    GPIO.add_event_callback(pin14, signal14)
    GPIO.add_event_detect(pin15, GPIO.RISING)
    GPIO.add_event_callback(pin15, signal15)
    try:
                thread.start_new_thread(myFunc, ())
    except:
                sys.stdout.write("Thread2 Error")
                sys.stdout.flush()

    while True:
	try:
        	perc4 = thread.start_new_thread(mq4.MQPercentage, ())
		perc5 = thread.start_new_thread(mq5.MQPercentage, ())
		perc6 = thread.start_new_thread(mq6.MQPercentage, ())
		perc9 = thread.start_new_thread(mq9.MQPercentage, ())
		time.sleep(2)
	except:
		sys.stdout.write("Thread Error")
		sys.stdout.flush()
	sys.stdout.write("\r")
        sys.stdout.write("\033[K")	
	#sys.stdout.write("LPG4: %g ppm ; LPG5: %g ppm ; LPG6: %g ppm ; LPG9: %g ppm " % (mq4.val["LPG4"], mq5.val["LPG5"], mq4.val["LPG4"], mq5.val["LPG5"])),
	sys.stdout.flush()

except Exception as e:
    	GPIO.cleanup()
	print("\nAbort by user", e)
    
