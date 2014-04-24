import socket 


#Mocked IP Addresses of Raspberry Pis
IP_addr = "1.1.1.1,2.2.2.2,3.3.3.3,4.4.4.4"



host = '' 
port = 50000 
backlog = 5 
size = 1024 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
s.listen(backlog) 
while 1: 
    client, address = s.accept() 
    client.send(IP_addr)
    client.close()