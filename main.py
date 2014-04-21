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
inputPins = {'takePhoto' : 8, 'takeVideo' : 10, 'takeLivestream' : 12, 'takeGroupPhoto' : 16}

root_dir = "../img/"
##End configurations
########

########
##Raspberry Pi Setup

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
camera = picamera.PiCamera()

##End Pi Setup
########
def read_socket(s):
    while True:
        data = s.recv(1024)
        if (data == '0'):
            take_photo(99)
        elif (data == '1'):
            take_video(99)

def sendIpAddr():
    HOST = 'unix4.andrew.cmu.edu'
    PORT = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    thread.start_new_thread(read_socket, (s,)) 
    return s

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
    base_filename = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H-%M-%S')
    filename = base_filename + "." + extension
    return (os.path.join(root_dir, filename), filename)

def upload_file_aws(filename, keyname):
    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.create_bucket(bucket_name)
    #bucks = conn.get_all_buckets()
    k = Key(bucket)
    k.key = keyname
    k.set_contents_from_filename(filename)    

def take_photo(channel):
    if (channel == 99):
        print "thanks to distributed server"
    print "in take_photo()"
    (filename, keyname) = generate_filename("jpg")
    GPIO.output(outputPins.get('takePhoto'), True)
    result = camera.capture(filename)
    time.sleep(1)
    upload_file_aws(filename, keyname)
    GPIO.output(outputPins.get('takePhoto'), False)


def take_video(channel):
    if (channel == 99):
        print "thanks to distributed server"
    if GPIO.input(channel):
        print "in take_video() - rising edge"
        GPIO.output(outputPins.get('takeVideo'), True)
        #(filename, heyname) = generate_filename("h264")
        #camera.start_recording(filename)
    else:
        print "in take_video() - falling edge"
        GPIO.output(outputPins.get('takeVideo'), False)
        #camera.stop_recording()


def setupTriggers(s):
    #bouncetime = ignore further edges for certain time period (specified in ms)
    def take_group_photo(channel):
        print "in take_group_photo()"
        s.sendall('0')

    GPIO.add_event_detect(inputPins.get('takePhoto'), GPIO.RISING, callback=take_photo, bouncetime=100)
    GPIO.add_event_detect(inputPins.get('takeVideo'), GPIO.BOTH, callback=take_video, bouncetime=100)
    GPIO.add_event_detect(inputPins.get('takeGroupPhoto'), GPIO.RISING, callback=take_group_photo, bouncetime=100)
    pass

def setup_folders():
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)

def main():
    print "STARTING"
    setup_folders()
    setupPins()
    testWifi()
    s = sendIpAddr()
    setupTriggers(s)

    while True:
        try:
            pass
        except:
            print "ERROR"
            s.close()
            GPIO.cleanup()
            exit(1)

if __name__ == "__main__":
    main()

