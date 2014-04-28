Carnegie Mellon University
18-549 Electrical & Computer Engineering Embedded Systems Capstone Project
Spring 2014

Group Members:
Adewale Desalu (adesalu)
Rishabh Alaap Singh (rasingh)
Vijay Iyengar (vijayj)
Vishalsai Daswani (vhd)

Project Description:
This project involves building a glove that allows you to take photos simply by making the symbolic picture sign, by connecting each thumb to the opposite hand's index finger. Also, with different modes, you can select picture mode, video modes, and even activate other cameras in the nearby area.

To run the whole system:
1. Run the java distributed server on "unix4.andrew.cmu.edu" with port 4863
    i. ssh <andrew_id>@unix4.andrew.cmu.edu
    ii. cd <folder_containing_server>/
    iii. javac Server.java
    iv. java Server

2. Boot up each Raspberry Pi and use as directed.
    i. Connect Raspberry Pi pins to the circuit as needed
    ii. Make sure WIFI dongle is connected
    iii. Make sure SD Card is inserted
    iv. Connect camera
    v. Connect to power


To configure Server:
1. Make sure configured to run on port 4863


To configure Raspberry Pi:
1. mkdir ~/snap
2. mkdir ~/snap/scripts
3. scp main.py pi@<ipaddr>:~/snap/scripts
4. scp configs.py pi@<ipaddr>:~/snap/scripts
5. vi ~/.profile
    add "sudo ~/snap/scripts/main.py" to the end of the file

6. Instal python lib "picamera"
    i. sudo apt-get install python-setuptools
    ii. sudo pip install picamera



Pin Configuration:
Output:
    3 - GREENLED
    5 - REDLED

Input:
    7 - TAKE_LIVESTREAM
    11 - TAKE_PHOTO
    13 - TAKE_VIDEO
    15 - TAKE_DISTRIBUTED_PHOTO

Voltages:
    1 - 3.3V
    9 - GND



What does main.py do:
1. Creates "imgs" folder if needed
2. Sets up the pin inputs and outputs
3. Checks if WIFI has been connected
4. Connects to SERVER on unix4.andrew.cmu.edu
5. Sets up the triggers that enable the camera using functionality


