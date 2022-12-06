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

clients = list()

def successConnect():
    join = {"command":"join"}
    return join


def leave():
    exit = {"command":"leave"}
    return exit

def commandlist():
    commands = (""" Command List\n
    1. Connect to the server application: /join <server_ip_add> <port>\n
    2. Disconnect to the server application: /leave\n
    3. Register a unique handle or alias: /register <handle>\n
    4. Send message to all: /all <message>\n
    5. Send direct message to a single handle: /msg <handle> <message> \n
    6. Request command help to output all Input Syntax commands for references: /?""")
    help = {"command":"help", "message": commands}
    return help

def register(data):
    person = {"command": "register", "handle": data[1]}
    return person

def sendToAll(data):
    message = " ".join(data[1:])
    print("Message: " + message)
    send = {"command": "all", "message": message}
    return send

def sendToReceiver(data):
    handle = "To " + data[1]
    message = " ".join(data[2:])
    print("Message: " + message)
    send = {"command": "msg", "handle": handle, "message": message}
    print(send)
    return send

def fromSender(data, name):
    handle = "From " + name
    message = " ".join(data[2:])
    print("Message: " + message)
    send = {"command": "msg", "handle": handle, "message": message}
    print(send)
    return send

def findPerson(address):
    for c in clients:
        if c[1] == address:
            name = c[0]
            return name

def findAddress(name):
    name = name.split()
    find = name[1]
    for c in clients:
        if c[0] == find:
            address = c[1]
            return address


# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 12345
s.bind((host, port))

while True:
    print("####### Server is listening #######")
    data, address = s.recvfrom(4096)
    print(data)
    print(address)
    print("\n\n 2. Server received: ", data.decode('utf-8'), "\n\n")

    data = data.decode('utf-8')
    data = data.split()

    #for the error messages, have to double check the test kit cuz i don't fully understand which
    #error messages pop up per situation
    if data[0] == '/join':
        try:
            if data[1] == host and int(data[2]) == port:
                command = json.dumps(successConnect())
                s.sendto(command.encode('utf-8'), address)
        except:
            print("Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number")
    elif data[0] == '/leave': 
        try:
            command = json.dumps(leave())
            s.sendto(command.encode('utf-8'), address)
        except:
            print("Error: Disconnection failed. Please connect to the server first.")           

    elif data[0] == '/?':
        command = json.dumps(commandlist())
        print(command)
        s.sendto(command.encode('utf-8'), address)

    elif data[0] == '/register':
        temp = list()
        temp.append(data[1])
        temp.append(address)
        print(temp)
        clients.append(temp)
        print(clients)
        #converts to json and sends the completion of command to client
        command = json.dumps(register(data))
        #s.sendto(command.encode('utf-8'), address)

        for c in clients:
            print(c[0])
            sendTo = c[1]
            s.sendto(command.encode('utf-8'), sendTo)
        print("Done registering")

    elif data[0] == '/all':
        command = json.dumps(sendToAll(data))
        ctr = 1
        for c in clients:
            print(c[0])
            sendTo = c[1]
            s.sendto(command.encode('utf-8'), sendTo)
            print("Sent to " + str(ctr))
            ctr += 1
        print("Done sending to all")
    elif data[0] == '/msg':
        senderName = findPerson(address)
        sender = json.dumps(fromSender(data, senderName))
        sender.replace("'", '"')
        se = json.loads(sender)
        print("Sender: " + se["handle"])

        receiver = json.dumps(sendToReceiver(data))
        receiver.replace("'", '"')
        r = json.loads(receiver)
        print("Receiver: " + r["handle"])
        
        s.sendto(receiver.encode('utf-8'), findAddress(se["handle"])) #receiver sees that message is from sender
        s.sendto(sender.encode('utf-8'), findAddress(r["handle"]))  #sender sees that message is sent to receiver

    

    """ 
    s_name = host.recv(1024)
    s_name = s_name.decode()
    print(s_name, "has connected to the chat room")
    host.send(s_name.encode())
    """
    
    """ 
    send_data = input("Type some text to send => ")
    s.sendto(send_data.encode('utf-8'), address)
    print("\n\n 1. Server sent : ", send_data,"\n\n")
    """