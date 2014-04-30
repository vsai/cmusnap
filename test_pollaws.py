from configs import *

import boto
from boto.s3.connection import S3Connection, Location
from boto.s3.key import Key

import sys, os, glob
import pprint

conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
lastModified = u''

#def magic():
    #group numbers that have just been added

    #upload to flickr all solos (

def getFilesAndData():
    #conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.create_bucket(bucket_name)
    blist = bucket.list()
    ordered = sorted(blist, key=lambda k: k.last_modified)
    print len(ordered)
    for i in ordered:
        print i.name, i.last_modified, type(i.last_modified)
    return
    
    for b in blist:
        print type(b)
        pprint.pprint(vars(b))
        break
    conn.close()


def pollForAWS():
    global lastModified
    print "polling for AWS"

    bucket = conn.get_bucket(bucket_name)
    blist = bucket.list()

    sortedFiles = sorted(blist, key=lambda k: k.last_modified)

    #ordered = sorted(blist, key=lambda k: k.last_modified)
    #ordered = ordered[::-1]
    
    def isNewer(f):
        return f.last_modified > lastModified

    def isSoloPic(f):
        return f.last_modified.startswith("2014_")
    
    newFiles = filter(isNewer, sortedFiles)
    solos = filter(isSoloPic, newFiles)
    print "solos = ", solos
    groups = filter(lambda f: not isSoloPic(f), newFiles)
    #groups = [ordered.remove(i) for i in solos]
    print "groups = ", groups
    #lastModified = ordered[0].last_modified

    if len(newFiles)>0:
        lastModified = newFiles[-1].last_modified





#def upload_file_aws(filename, keyname):
#    conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
#    bucket = conn.create_bucket(bucket_name)
#    k = Key(bucket)
#    k.key = keyname
#    k.set_contents_from_filename(filename)


if __name__ == "__main__":
    getFilesAndData()



