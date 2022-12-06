""" 
import socket
import json

clientsock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

msg=input()
clientsock.sendto(msg.encode("utf-8"),('127.0.0.1', 12345))
data,addr=clientsock.recvfrom(4096)
print("Server Says")
print(str(msg))
clientsock.close()
"""

import socket
import json

if __name__ == "__main__":
    host = input(str("Enter Address: "))
    port = int(input(str("Enter Port Number: ")))
    addr = (host, port)

    """ Creating the UDP socket """
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        data = input("Enter a word: ")

        if data == "!EXIT":
            data = data.encode("utf-8")
            client.sendto(data, addr)

            print("Disconneted from the server.")
            break

        data = data.encode("utf-8")
        client.sendto(data, addr)

        data, addr = client.recvfrom(1024)
        data = data.decode("utf-8")
        print(f"Server: {data}")