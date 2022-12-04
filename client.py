import socket
import json

clientsock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg=input()
clientsock.sendto(msg.encode("utf-8"),('127.0.0.1', 12345))
data,addr=clientsock.recvfrom(4096)
print("Server Says")
print(str(msg))
clientsock.close()