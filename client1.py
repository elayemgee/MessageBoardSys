import socket
import json
import threading

UDP_MAX_SIZE = 65535
    
def listen(s: socket.socket):
    while True:
        msg = s.recv(UDP_MAX_SIZE)
        x = msg.decode('utf-8')
        comm = json.loads(x)
        if comm["command"] == "leave":
            break
        if comm["command"] == "help":
            print('\r\r' + comm["message"])
        if comm["command"] == "register":
            x.replace("'", '"')
            print('\r\r' + "Welcome " + comm["handle"])
            
        if comm["command"] == "all":
            x.replace("'", '"')
            print('\r\r' + comm["message"])
        if comm["command"] == "msg":
            x.replace("'", '"')
            print('\r\r' + "[" + comm["handle"] + "]: " + comm["message"])   
    s.close()
    print("Connection closed. Thank you!")

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

threading.Thread(target=listen, args=(s,), daemon=True).start()
s.send('__join'.encode('ascii'))

command = input("")
all_words = command.split()
s.send(command.encode())

# Let's send data through UDP protocol

while True:
    """
    x = s.recv(4096)
    x = x.decode('utf-8')
    comm = json.loads(x)
    """ 
    command = input("")
    s.send(command.encode('utf-8'))
    

# close the socket

