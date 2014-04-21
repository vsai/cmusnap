#!/usr/bin/python

import socket

def sendIpAddr():
    HOST = 'unix4.andrew.cmu.edu'
    PORT = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.close()

if __name__ == "__main__":
    sendIpAddr()
