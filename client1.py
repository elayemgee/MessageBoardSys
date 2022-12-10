import socket
import json
import threading
import sys

UDP_MAX_SIZE = 65535
connected = False
username = None
server_addr = '127.0.0.1'
server_port = 12345
server = (server_addr, server_port)

def commandlist():
    print(""" Command List\n
    1. Connect to the server application: /join <server_ip_add> <port>\n
    2. Disconnect to the server application: /leave\n
    3. Register a unique handle or alias: /register <handle>\n
    4. Send message to all: /all <message>\n
    5. Send direct message to a single handle: /msg <handle> <message> \n
    6. Request command help to output all Input Syntax commands for references: /?""")

def set_name(name):
    global username
    username = name
    
def json_join():
    join = {"command":"join"}
    return join

def json_leave():
    leave = {"command":"leave"}
    return leave

def json_register(name):
    person = {"command": "register", "handle": name}
    return person

def json_all(command):
    message = " ".join(command[1:])
    withHandle = username + ": " + message
    send = {"command": "all", "message": withHandle}
    return send

def json_sendone(data):
    handle = data[1]
    message = " ".join(data[2:])
    send = {"command": "msg", "handle": handle, "message": message}
    return send
    
def listen(s: socket.socket):
    global spark
    spark = True
    while spark:
        msg = s.recv(UDP_MAX_SIZE)
        #msg = s.recvfrom(4096)
        x = msg.decode('utf-8')
        comm = json.loads(x)
        
        if comm["command"] == 'join':
            #s.connect((host, port))
            print("Connection to the Message Board Server is successful!")
        if comm["command"] == "leave":
            global connected
            connected = False
            break
        if comm["command"] == "help":
            print('\r\r' + comm["message"])
        if comm["command"] == "register":
            x.replace("'", '"')
            print('\r\r' + "Welcome " + comm["handle"] + "!")   
            set_name(comm["handle"])
        if comm["command"] == "all":
            x.replace("'", '"')
            print('\r\r' + comm["message"])
        if comm["command"] == "msg":
            x.replace("'", '"')
            if comm["handle"] != username:
                print('\r\r' + "[To " + comm["handle"] + "]: " + comm["message"])
            else:
                print('\r\r' + "[From " + comm["handle"] + "]: " + comm["message"])

    s.close()
    print("Connection closed. Thank you!")   
    return None
    
# Let's send data through UDP protocol
while True:
    command = input("")

    #client must be connected first to server
    if connected == False and command == "/join 127.0.0.1 12345":
        #create socket for server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        connected = True
        join = json.dumps(json_join())
        s.sendto(join.encode('utf-8'), server)
        #s.send(command.encode('utf-8'))
       # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
       # s.connect(('127.0.0.1', 12345))
        threading.Thread(target=listen, args=(s,), daemon=True).start()
        #print("Connection to the Message Board Server is successful!")
    elif command == "/?": 
        commandlist()
    elif connected == True:
        command = command.split()
        if len(command) == 1 and command[0] == '/leave':
            leave = json.dumps(json_leave())
            s.sendto(leave.encode('utf-8'), server)
        elif len(command) == 2 and command[0] == '/register':
            register = json.dumps(json_register(command[1]))
            s.sendto(register.encode('utf-8'), server)
        elif len(command) >= 2 and command[0] == '/all':
            send_all = json.dumps(json_all(command))
            s.sendto(send_all.encode('utf-8'), server)
        elif len(command) >= 3 and command[0] == '/msg':
            send_one = json.dumps(json_sendone(command))
            s.sendto(send_one.encode('utf-8'), server)
        else:
            print("error")
    else:
        print("error")

