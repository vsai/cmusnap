#!/usr/bin/python

import os
import sys
import time
import datetime
import urllib2

import RPi.GPIO as GPIO
import picamera

import boto
from boto.s3.connection import S3Connection, Location
from boto.s3.key import Key


########
##Configurations

from configs import *
#This imports
# - AWS_ACCESS_KEY_ID
# - AWS_SECRET_ACCESS_KEY
# - bucket_name

#outputPins = {'takePhoto' : 3, 'takeVideo' : 5, 'takeLivestream' : 7, \
#                'wifiError' : 19, 'cameraError' : 21, 'generalError' : 23}
#inputPins = {'takePhoto' : 11, 'takeVideo' : 12, 'takeLivestream' : 13}

outputPins = {'takePhoto' : 3, 'takeVideo' : 3, 'takeLivestream' : 3, \
                'wifiError' : 19, 'cameraError' : 19, 'generalError' : 19}
inputPins = {'takePhoto' : 8, 'takeVideo' : 10, 'takeLivestream' : 12}

##End configurations
########

########
##Raspberry Pi Setup

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
camera = picamera.PiCamera()

##End Pi Setup
########

def testWifi():
    GPIO.output(outputPins.get('wifiError'), True)
    time.sleep(1)
    while True:
        #while wifi ERROR led is lit up, we know
        #that it is trying to set it up
        try:
            urllib2.urlopen("http://www.google.com").close()
        except urllib2.URLError:
            print "Not Connected"
            time.sleep(1)
        else:
            print "Connected"
            GPIO.output(outputPins.get('wifiError'), False)
            return

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
    root_dir = "../img/"
    base_filename = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')
    filename = base_filename + "." + extension
    return (os.path.join(root_dir, filename), base_filename+"."+extension)

def upload_file_aws(filename, keyname):
    # def percent_cb(complete, total):
    #     print complete, total 
    #     sys.stdout.write('.')
    #     sys.stdout.flush()

    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.create_bucket(bucket_name)
    #bucks = conn.get_all_buckets()
    k = Key(bucket)
    k.key = keyname
    k.set_contents_from_filename(filename)
    #k.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)


def take_photo(channel):
    print "in take_photo()"
    (filename, keyname) = generate_filename("jpg")
    GPIO.output(outputPins.get('takePhoto'), True)
    result = camera.capture(filename)
    # time.sleep(1)
    upload_file_aws(filename, keyname)
    GPIO.output(outputPins.get('takePhoto'), False)


def take_video(channel):
    if GPIO.input(channel):
        print "in take_video() - rising edge"
        GPIO.output(outputPins.get('takeVideo'), True)
    else:
        print "in take_video() - falling edge"
        GPIO.output(outputPins.get('takeVideo'), False)

def setupTriggers():
    #bouncetime = ignore further edges for certain time period (specified in ms)
    
    GPIO.add_event_detect(inputPins.get('takePhoto'), GPIO.RISING, callback=take_photo, bouncetime=100)
    
    #bouncetime is set to 0 for video so that it will ALWAYS detect falling edge, 
    #and so never continue recording while disconnected
    GPIO.add_event_detect(inputPins.get('takeVideo'), GPIO.BOTH, callback=take_video, bouncetime=10)
    pass



def main():
    print "STARTING"
    setupPins()
    testWifi()
    setupTriggers()

    while True:
        try:
            pass
        except:
            print "ERROR"
            GPIO.cleanup()
            exit(1)

if __name__ == "__main__":
    main()
