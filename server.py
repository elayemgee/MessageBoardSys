import socket
import json

serversock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversock.bind(('127.0.0.1', 12345))

while True:
    data,addr = serversock.recvfrom(4096)
    print(str(data))
    serversock.sendto(data,addr)


""" NOTES
import socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


host = input("Enter The Server Ip: ")
port = input("Enter The Server Port: ")

serversocket.bind((host, port)) 

serversocket.listen(10)

while True :
    clientsocket, address = serversocket.accept()

    print("Received Connection From %s" % str(address))

    message = 'Connection Established' + "\r\n"
    clientsocket.send(message.encode("ascii"))

    clientsocket.close()
    """