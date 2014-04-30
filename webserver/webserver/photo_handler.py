# boto communication
import boto
import sys, os, glob
from boto.s3.key import Key

# stitching
import picstitch

# flickr communication
import flickrapi

# other dependencies
import string, time
import collections.Counter

# AWS Config setup
LOCAL_PATH = os.getcwd() + "/static/temp"
AWS_ACCESS_KEY_ID = "AKIAJQO7AI5XW54UN5UQ"
AWS_SECRET_ACCESS_KEY = "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"
bucket_name = AWS_ACCESS_KEY_ID.lower() + "-vhd-549-bucket_demo"
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
lastModified = "2014-04-30T09:59:24.000Z"


# Flickr Setup
flickr_api_key = "75f7e59201f9b055d876367e5bb3bb9b"
flickr_api_secret = "72aa38d4a39c849d"
flickr = flickrapi.FlickrAPI(flickr_api_key, flickr_api_secret)

(token, frob) = flickr.get_token_part_one(perms="write")
if not token: raw_input("Press ENTER after auth")
flickr.get_token_part_two((token,frob))


def pollForAWS():
  global lastModified

  print "got into this thing!"

  bucket = conn.get_bucket(bucket_name)

  blist = bucket.list()
  #ordered = sorted(blist, key=lambda k: k.last_modified)
  #ordered = ordered[::-1]

  ordered = filter(lambda x: x.last_modified > lastModified, blist)

  #refMap = map(lambda i: i.name, ordered)

  solos = filter(lambda i:i.last_modified.startswith("2014"),ordered)
  print "solos = ", solos

  #groups = [ordered.remove(i) for i in solos]
  groups = Counter(ordered) - Counter(solos)
  print "groups = ", groups


  # update lastModified
  #lastModified = ordered[0].last_modified


def pullFromAWS(groupID):
  print "waiting 3 seconds to pull"

  time.sleep(3) ## TODO: CHANGE THIS WHEN WE GET CONFIRMATION FROM PIS
  bucket = conn.get_bucket(bucket_name)

  # clean the 'temp' folder
  cleanTemp()

  # Filter only photos of this group
  group_list = [item for item in bucket.list() if str(item.key).startswith("%s_" % groupID)]

  for l in group_list:
    keyString = str(l.key)

    l.get_contents_to_filename("/".join([LOCAL_PATH, keyString]))
    print "downloaded " + keyString

  # Finally, stitch the images
  imgs = glob.glob(LOCAL_PATH + "/*")
  picstitch.stitch(imgs)

  # By convention, now that we stitch the image and save it to temp/res.jpg
  # Now, upload it!
  upload(LOCAL_PATH + "/res.jpg")

def uploadCallback(progress, done):
  if done:
    print "Uploaded!"
  else:
    print "At %s%%" % progress

def upload(url):
  flickr.upload(filename=url, callback=uploadCallback)


### HELPERS ###

def cleanTemp():
  files = glob.glob(LOCAL_PATH + '/*')
  for f in files:
    os.remove(f)

  print "cleaned temp folder"





