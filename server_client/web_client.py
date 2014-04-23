""" Mock web server code that sends the main server a list of clients to be activated/deactivated. The format is csv where each value is:
    <clientNickname>:<0 to deactivate, 1 to activate>

    A valid input would be:
        0:1,1:0,2:0,3:1,5:0

    This would activate Pis 0 and 3 and deactivate 1,2, and 5. Pi 4 would be    unchanged. """

import socket, thread

def read_socket(s):
    while (True):
        data = s.recv(1024)
        if (data == '0'):
            pass
        elif (data == '1'):
            pass

HOST = 'unix4.andrew.cmu.edu'   # The remote host
PORT = 5000                     # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
thread.start_new_thread(read_socket, (s,))

while (True):
    var = raw_input()
    s.sendall(var + '\n') 

s.close()
