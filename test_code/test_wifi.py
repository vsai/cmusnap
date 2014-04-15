#!/usr/bin/python

import os
import time
import urllib2

#os.system("gpio mode 6 out && gpio mode 5 out")
print "helloworld"

while True:
    try:
        urllib2.urlopen("http://www.google.com").close()
    except urllib2.URLError:
        print "Not Connected"
        #os.system("gpio write 6 0 && gpio write 5 1")
        time.sleep(1)
    else:
        print "Connected"
        #os.system("gpio write 6 1 && gpio write 5 0")
        break

