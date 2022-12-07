import socket
import json
import threading
import sys

UDP_MAX_SIZE = 65535
spark = True
    
def listen(s: socket.socket):
    global spark
    spark = True
    while spark:
        msg = s.recv(UDP_MAX_SIZE)
        x = msg.decode('utf-8')
        comm = json.loads(x)
        if comm["command"] == '/join':
            s.connect((host, port))
            print("Connection to the Message Board Server is successful!")
        if comm["command"] == "leave":
            spark = False
            break
        if comm["command"] == "help":
            print('\r\r' + comm["message"])
        if comm["command"] == "register":
            x.replace("'", '"')
            print('\r\r' + "Welcome " + comm["handle"] + "!")      
        if comm["command"] == "all":
            x.replace("'", '"')
            print('\r\r' + comm["message"])
        if comm["command"] == "msg":
            x.replace("'", '"')
            print('\r\r' + "[" + comm["handle"] + "]: " + comm["message"])

    s.close()
    print("Connection closed. Thank you!")   
    return None
    
    

# Create socket for server
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
thread = threading.Thread(target=listen, args=(s,), daemon=True)


connect = input("")
all_words = connect.split()
if len(all_words) == 3:
    first = all_words[0]
    host = all_words[1]
    port = int(all_words[2])

if first == '/join':
    s.connect((host, port))
    print("Connection to the Message Board Server is successful!")
    thread.start()
    s.send('__join'.encode('ascii'))
else:
    print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number.")

""" 
command = input("")
all_words = command.split()
s.send(command.encode())
"""

# Let's send data through UDP protocol

while True:
    """
    x = s.recv(4096)
    x = x.decode('utf-8')
    comm = json.loads(x)
    """ 

    command = input("")
    #needs to be edited so that the correct ip address and port number are used to connect to server
    if command == "/join 127.0.0.1 12345": 
        #s.send(command.encode('utf-8'))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('127.0.0.1', 12345))
        threading.Thread(target=listen, args=(s,), daemon=True).start()
        print("Connection to the Message Board Server is successful!")
    else:
        s.send(command.encode('utf-8'))


    

# close the socket

