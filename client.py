import socket
import json
import threading

UDP_MAX_SIZE = 65535
connected = False
username = None
server_addr = '127.0.0.1'
server_port = 12345
server = (server_addr, server_port)

def commandlist():
    print(""" Command List
    1. Connect to the server application: /join <server_ip_add> <port>
    2. Disconnect to the server application: /leave
    3. Register a unique handle or alias: /register <handle>
    4. Send message to all: /all <message>
    5. Send direct message to a single handle: /msg <handle> <message> 
    6. Request command help to output all Input Syntax commands for references: /?""")

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

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
    #withHandle = username + ": " + message
    send = {"command": "all", "message": message}
    return send

def json_sendone(data):
    handle = data[1]
    message = " ".join(data[2:])
    send = {"command": "msg", "handle": handle, "message": message}
    return send

def json_error(message):
    send = {"command": "error", "message": message}
    return send

def listen(s: socket.socket):
    while True:
        #msg = s.recv(UDP_MAX_SIZE)
        x, server = s.recvfrom(1024)
        #x = msg.decode('utf-8')
        #comm = json.loads(x)
        comm = json.loads(x)
        global connected
        
        if comm["command"] == 'join':
            #s.connect((host, port))
            connected = True
            print("Connection to the Message Board Server is successful!")
        if comm["command"] == "leave":
            connected = False
            s.close()
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
            break
        if comm["command"] == "help":
            print('\r\r' + comm["message"])
        if comm["command"] == "register":
            #x.replace("'", '"')
            print('\r\r' + "Welcome " + comm["handle"] + "!")   
            set_name(comm["handle"])
        if comm["command"] == "all":
            #x.replace("'", '"')
            print('\r\r' + comm["message"])
        if comm["command"] == "msg":
            print('\r\r' + comm["message"])
            #x.replace("'", '"')
            """
            if comm["handle"] != username:
                print('\r\r' + "[To " + comm["handle"] + "]: " + comm["message"]) #sender's end
            else:
                print('\r\r' + "[From " + comm["handle"] + "]: " + comm["message"]) #receiver's end
            """
        if comm["command"] == "error":
            print('\r\r' + comm["message"])
        
    print("Connection closed. Thank you!")   
    return None
    
# Let's send data through UDP protocol
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

while True:
    command = input("")

    #client must be connected first to server
    #/join 127.0.0.1 12345
    comm = command.split()
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    if connected == False and command == '/join 127.0.0.1 12345':
        #create socket for server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        join = json.dumps(json_join())
        #s.connect((comm[1], int(comm[2])))
        connected = True
        threading.Thread(target=listen, args=(s,), daemon=True).start()
        s.sendto(join.encode('utf-8'), server)

    elif command == "/?": 
        commandlist()
    elif connected == True:
        command = command.split()
        if command[0] == '/leave':
            if len(command) == 1:
                #threading.Thread(target=listen, args=(s,), daemon=True).start()
                leave = json.dumps(json_leave())
                s.sendto(leave.encode('utf-8'), server)
                username = None
            else:
                print("Error: Command parameters do not match or is not allowed.")
                
        elif command[0] == '/register':
            if len(command) == 2:
                if username == None:
                    register = json.dumps(json_register(command[1]))
                    s.sendto(register.encode('utf-8'), server)
                else:
                    print("Error: Registration failed. Already connected to server")
            else:
                print("Error: Command parameters do not match or is not allowed.")

        elif command[0] == '/all':
            if len(command) >= 2 and username != None:
                send_all = json.dumps(json_all(command))
                s.sendto(send_all.encode('utf-8'), server)
            elif username == None:
                print("Error: You are not registered yet.")
            else:
                print("Error: Command parameters do not match or is not allowed.")
            
        elif command[0] == '/msg':
            if username == None:
                print("Error: You are not registered yet.")
               
            elif len(command) >= 3:
                send_one = json.dumps(json_sendone(command))
                s.sendto(send_one.encode('utf-8'), server)
            else:
                print("Error: Command parameters do not match or is not allowed.")
                
        elif command[0] == '/join':
            print("Error: You are connected already.")
            
        else:
            print("Error: Command not found.")
    elif connected == False:
        if command[0] != '/':
            print("Error: Command not found.")
        elif comm[0] == '/join':
            if len(comm) != 3:
                print("Error: Command parameters do not match or is not allowed.")
            else:
                print("here in else")
                ip = comm[1]
                port = comm[2]
                #if there's any alphabetic character in the string
                if (any(c.isalpha() for c in ip)) or (any(c.isalpha() for c in port)):
                    print("Error: Command parameters do not match or is not allowed.")
                #this checks if ip is valid or port length is not 5 digits 
                elif validate_ip(ip) == False or (len(port) != 5) or port != server_port or ip != server_addr:
                    print("Connection to the Message Board Server has failed! Please check IP Address and Port Number.")
            
        elif comm[0] == '/leave':
            print("Error: Disconnection failed. Please connect to the server first.")

        elif comm[0] == '/register' or comm[0] == '/all' or comm[0] == '/msg':
            print("Error: You are not connected to the server yet.")
            
        else:
            print("Error: Command not found.")
            


