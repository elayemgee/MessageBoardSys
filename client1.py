import socket
import json

def askInput():
    command = input("")
    s.send(command.encode())

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

connect = input("")
all_words = connect.split()
if len(all_words) == 3:
    first = all_words[0]
    host = all_words[1]
    port = int(all_words[2])

if first == '/join':
    s.connect((host, port))
    print("Connection to the Message Board Server is successful!")
else:
    print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

command = input("")
all_words = command.split()
s.send(command.encode())

# Let's send data through UDP protocol

while True:
    x = s.recv(4096)
    x = x.decode('utf-8')
    comm = json.loads(x)

    if comm["command"] == "leave":
        break
    if comm["command"] == "help":
        print(comm["message"])
    if comm["command"] == "register":
        x.replace("'", '"')
        print("Welcome " + comm["handle"])
        
    if comm["command"] == "all":
        x.replace("'", '"')
        print(comm["message"])
        #concern: idk how to make it so that multiple people can receive the same message at the same time

    askInput()
""" 
    if comm["command"] == "msg":
        x.replace("'", '"')
        print("[" + comm["handle"] + "]: " + comm["message"])   
"""
    

# close the socket
s.close()
print("Connection closed. Thank you!")
