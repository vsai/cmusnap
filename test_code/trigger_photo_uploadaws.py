#!/usr/bin/python

import string
import random
import os

import picamera
#from time import sleep
import time
import datetime

import boto
import sys
from boto.s3.connection import S3Connection, Location
from boto.s3.key import Key

AWS_ACCESS_KEY_ID = ""
AWS_SECRET_ACCESS_KEY = ""
bucket_name = AWS_ACCESS_KEY_ID.lower() + "-vhd-549-bucket"

def id_generator():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H:%M:%S')

root_dir = "../img/"
filename = id_generator() + ".jpg"
local_store_filename = os.path.join(root_dir, filename) 

#Click the photo
camera = picamera.PiCamera()
result = camera.capture(local_store_filename)

print "uploading filename: %s, to bucket: %s"%(filename, bucket_name)

#boto.set_stream_logger('foo')
conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = conn.create_bucket(bucket_name)

bucks = conn.get_all_buckets()
#print "List of all buckets: "
#print bucks

def percent_cb(complete, total):
    print complete, total 
    sys.stdout.write('.')
    sys.stdout.flush()

k = Key(bucket)
k.key = filename
k.set_contents_from_filename(local_store_filename)
#k.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)

