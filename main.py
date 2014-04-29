#!/usr/bin/python

import os
import sys
import time
import datetime
import urllib2
import socket
import RPi.GPIO as GPIO
import picamera
import thread
from threading import Lock

import boto
from boto.s3.connection import S3Connection, Location
from boto.s3.key import Key

def shutdown():
    print 'Shutting down Pi'
    os.system('sudo shutdown -h now')

########
##Configurations

from configs import *
#This imports
# - AWS_ACCESS_KEY_ID
# - AWS_SECRET_ACCESS_KEY
# - bucket_name

outputPins = {'takePhoto' : 3, 'takeVideo' : 3, 'takeLivestream' : 3, \
                'wifiError' : 5, 'cameraError' : 5, 'generalError' : 5}
inputPins = {'takePhoto' : 11, 'takeVideo' : 12, 'takeLivestream' : 7, 'takeGroupPhoto' : 15}

HOST = 'unix4.andrew.cmu.edu'
PORT = 4863
root_dir = "../img/"
##End configurations
########

########
##Raspberry Pi Setup
CONNECTED_WIFI = False
CONNECTED_SERVER = False
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
camera_lock = Lock()
try:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
except:
    print 'Camera not found.'
    shutdown()


##End Pi Setup
########
def read_socket(s):
    """ Attempts to read from server """
    while True:
        data = s.recv(1024)
        if not data:
            break
        if (data == '0'):
            take_photo(99, distributed=True)
        elif (data == '1'):
       take_video1(1, distribued=True)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    testWifi(s)

def connectToServer(s):
    """ Attempts to connect to server """
    GPIO.output(outputPins.get('wifiError'), True)
    global CONNECTED_SERVER
    while True:
        try:
            s.connect((HOST, PORT))
            CONNECTED_SERVER = True
            GPIO.output(outputPins.get('wifiError'), False)
            print "Successfully connected to server!"
            break

        except:
            print "Could not connect to server. Will try again in 5 seconds"
            for i in xrange(5):
                GPIO.output(outputPins.get('wifiError'), False)
                time.sleep(0.5)
                GPIO.output(outputPins.get('wifiError'), True)
                time.sleep(0.5)
                
    read_socket(s)

def sendIpAddr():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # After Wifi is established, connects to server, then starts reading from server
    thread.start_new_thread(testWifi, (s,))
    return s

def testWifi(s):
    GPIO.output(outputPins.get('wifiError'), True)
    time.sleep(1)
    while True:
        #while wifi ERROR led is lit up, we know
        #that it is trying to set it up
        try:
            urllib2.urlopen("http://www.google.com").close()
        except urllib2.URLError:
            print "Not Connected"
            for i in xrange(5):
                GPIO.output(outputPins.get('wifiError'), False)
                time.sleep(0.5)
                GPIO.output(outputPins.get('wifiError'), True)
                time.sleep(0.5)
        else:
            print "Connected"
            CONNECTED_WIFI = True
            GPIO.output(outputPins.get('wifiError'), False)
            break
    
    connectToServer(s)           

def setupPins():
    #validates if the pin set up mentioned in configs is alright
    #sets up pins as mentioned in the pin config setup
    outPins = set(outputPins.values())
    inPins = set(inputPins.values())

    def validatePins():
        allPins = outPins.union(inPins)
        if (len(outPins) + len(inPins) != len(allPins)):
            print "Overlapping pins input and output"
            return False
        else:
            print "Successful validation of pins"
            return True

    if (validatePins()):
        for pin in outPins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
        for pin in inPins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        print "successfully setup pins"
        return True
    else:
        print "ERROR: input configuration of pins provided is incorrect"
        print "EXITING PROGRAM"
        exit(1)

def generate_filename(extension):
    base_filename = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
    filename = base_filename + "." + extension
    return (os.path.join(root_dir, filename), filename)

def upload_file_aws(filename, keyname):
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.create_bucket(bucket_name)
    k = Key(bucket)
    k.key = keyname
    k.set_contents_from_filename(filename)

def take_photo(channel, distributed=False):
    if distributed:
        print "thanks to distributed server"
    if (channel != 99 and camera_lock.locked()):
        #if not from distributed server and camera is being used, ignore take_photo
        #ALWAYS ACCEPT REQUESTS from DISTRIBUTED SERVER
	return
        #break
    camera_lock.acquire()
    print "in take_photo()"
    (filename, keyname) = generate_filename("jpg")
    GPIO.output(outputPins.get('takePhoto'), True)
    result = camera.capture(filename)
    time.sleep(1)
    camera_lock.release()
    upload_file_aws(filename, keyname)
    GPIO.output(outputPins.get('takePhoto'), False)


def take_video(channel, distributed=False):
    print "IN TAKE_VIDEO - function activated"
    if distributed:
        print "video - thanks to distributed server"
        print "not supported yet"
        return
	#break

    if GPIO.input(channel):
        print "IN GPIO INPUT CHANNEL"
        if (camera_lock.locked()):
            print "CAMERA_LOCKED"
            return
            #break
        camera_lock.acquire()
        print "ACQUIRING CAMERA LOCK"
        print "in take_video() - rising edge"
        GPIO.output(outputPins.get('takeVideo'), True)
        (filename, keyname) = generate_filename("h264")
        camera.start_recording(filename)
    else:
        if (not camera_lock.locked()):
            return
            #break
        print "in take_video() - falling edge"
        GPIO.output(outputPins.get('takeVideo'), False)
        camera.stop_recording()
        camera_lock.release()


def setupTriggers(s):
    #bouncetime = ignore further edges for certain time period (specified in ms)
    def take_group_photo(channel):
        if CONNECTED_SERVER:
            print "in take_group_photo()"
            s.sendall('0')
        else:
            print "not connected to server"

    GPIO.add_event_detect(inputPins.get('takePhoto'), GPIO.RISING, callback=take_photo, bouncetime=1000)
    GPIO.add_event_detect(inputPins.get('takeVideo'), GPIO.BOTH, callback=take_video, bouncetime=100)
    print "Setup takeVideo on pin: %d"%(inputPins.get('takeVideo'))
    print take_video
    GPIO.add_event_detect(inputPins.get('takeGroupPhoto'), GPIO.RISING, callback=take_group_photo, bouncetime=1000)
    pass

def setup_folders():
    #creates image directory if not ready
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)

def main():
    print "STARTING"
    setup_folders()
    setupPins()
    s = sendIpAddr() #calls testwifi
    setupTriggers(s)
    print " Done setting triggers "
    
    try:
        while True:
            time.sleep(5)
            pass
        #pass
    except:
        pass
    finally:
        print "ERROR or KEYBOARD EXIT - exiting program"
        s.close()
        GPIO.cleanup()
        exit(1)

if __name__ == "__main__":
    main()

