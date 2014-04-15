import socket
import time

HOST = 'unix4.andrew.cmu.edu'   # The remote host
PORT = 5000                     # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
count = 0
while (count < 10):
    s.sendall('Hello, world')
    data = s.recv(1024)
    print 'Received', repr(data)
    time.sleep(1)
    count += 1
s.close()
