import socket

HOST = '192.168.1.109'          # The remote host
PORT = 5000                     # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall('2')
while (True):
    data = s.recv(1024)
    print 'Received', repr(data)
    pass
s.close()
