import socket, thread

def read_stdin(s):
    while (True):
        var = raw_input()
        if (var == 'Photo' or var == 'Video'):
            s.sendall(var)
        return

HOST = 'unix4.andrew.cmu.edu'   # The remote host
PORT = 5000                     # The same port as used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
count = 0
thread.start_new_thread(read_stdin, (s,))
while (True):
    #s.sendall('Hello, world')
    data = s.recv(1024)
    if (data == 'Photo'):
        print "Take a photo"
    elif (data == 'Video'):
        print "Take a video"
s.close()
