# THANKS: http://www.laurentluce.com/posts/upload-and-download-files-tofrom-amazon-s3-using-pythondjango/

# boto communication
import boto
import sys, os
from boto.s3.key import Key

# Other dependencies
import string

def download_to_local():
  LOCAL_PATH = os.getcwd() + "/temp/"
  AWS_ACCESS_KEY_ID = "AKIAJQO7AI5XW54UN5UQ"
  AWS_SECRET_ACCESS_KEY = "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"
  bucket_name = AWS_ACCESS_KEY_ID.lower() + "-vhd-549-bucket"

  conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
  bucket = conn.get_bucket(bucket_name)

  bucket_list = bucket.list()

  for l in bucket_list:
    keyString = str(l.key)
    print "keyString = ", keyString

  #check if file exists locally, if not download it
  if not os.path.exists(LOCAL_PATH+keyString):
    l.get_contents_to_filename(LOCAL_PATH+keyString)
    print "downloaded " + keyString

  print "\n\ndone! :)"

download_to_local()