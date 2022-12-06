""" 
import socket
import json

serversock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serversock.bind(('127.0.0.1', 12345))

while True:
    data,addr = serversock.recvfrom(4096)
    print(str(data))
    serversock.sendto(data,addr)
"""
import socket
import json

if __name__ == "__main__":
    host = socket.gethostname()

    addr = (host, 12345)
    sockinfo = socket.getnameinfo(addr,socket.NI_NUMERICSERV)[1]
    print(sockinfo)
    port =12345
    """ Creating the UDP socket """
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    """ Bind the host address with the port """
    server.bind((host, port))
    
    while True:
        data, addr = server.recvfrom(1024)
        data = data.decode("utf-8")
        print(data)

        if data == "!EXIT":
            print("Client disconnected.")
            break

        print(f"Client: {data}")

        data = data.upper()
        data = data.encode("utf-8")
        server.sendto(data, addr)
