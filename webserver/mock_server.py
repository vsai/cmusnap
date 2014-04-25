import socket, time


#Mocked IP Addresses of Raspberry Pis
IP_addr = "1.1.1.1,2.2.2.2,3.3.3.3,4.4.4.4"


for i in range(0,10):
  print str(i)
  time.sleep(2)



host = '' 
port = 50000 
backlog = 5 
size = 1024 
print "starting server..."
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.bind((host,port)) 
print "...socket found! ", s
s.listen(backlog) 

while 1: 
    client, address = s.accept() 

    for i in range(0,10):
      client.send(str(i))
      time.sleep(2)
    

    client.close()