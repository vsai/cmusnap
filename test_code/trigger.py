#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

print("SYS: Raspberry Pi Initializing")

# Setup GPIO Port pin 11 as an input (could optionally configure pull up/down)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Loop forever constantly checking the input pin to see if it has been brought low
while True:
    input_value = GPIO.input(11)        # Read the status of input Pin 11
    if input_value == True:            # If the pin is low (i.e. button has been pushed)
        print("\n\n\nTrigger: CLICK PICTURE\n")
	os.system("./photo_upload.py finally")
        time.sleep(3)

    else: 
        print("waiting...")
    while (input_value == True): # Keep checking status of pin until it is no longer low
        input_value = GPIO.input(11)

# We never get here, but if we did, we should do this

# Return all GPIO pins back to their default state of being inputs with no pull up/down
GPIO.cleanup()
