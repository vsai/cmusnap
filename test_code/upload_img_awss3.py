#!/usr/bin/python

import boto
import sys
from boto.s3.connection import S3Connection, Location
from boto.s3.key import Key


AWS_ACCESS_KEY_ID = "AKIAJQO7AI5XW54UN5UQ"
AWS_SECRET_ACCESS_KEY = "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"
bucket_name = AWS_ACCESS_KEY_ID.lower() + "-vhd-549-bucket"


filename = sys.argv[1]
print "uploading filename: %s, to bucket: %s"%(filename, bucket_name)

#boto.set_stream_logger('foo')

conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
bucket = conn.create_bucket(bucket_name)

bucks = conn.get_all_buckets()
print "List of all buckets: "
print bucks

def percent_cb(complete, total):
    sys.stdout.write('.')
    sys.stdout.flush()

k = Key(bucket)
k.key = filename
k.set_contents_from_filename(filename, cb=percent_cb, num_cb=10)

