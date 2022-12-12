import socket
import json

clients = list()

def successConnect():
    join = {"command":"join"}
    return join

def leave():
    exit = {"command":"leave"}
    return exit

def register(data):
    person = {"command": "register", "handle": data[1]}
    return person

def sendToAll(data, name):
    message = " ".join(data[1:])
    withHandle = name + ": " + message
    print("Message: " + withHandle)
    send = {"command": "all", "message": withHandle}
    return send

def fromSender(message, name): #sets handle as person who sent the message
    send = {"command": "msg", "handle": name, "message": message}
    return send

def findPerson(address): #find person's name based on address
    for c in clients:
        if c[1] == address:
            name = c[0]
            return name

def findAddress(name): #find address based on name
    for c in clients:
        if c[0] == name:
            address = c[1]
            return address

def findClientIndex(address):
    ctr = 0
    index = 0
    for c in clients:
            if c[1] == address:
                index = clients.index(c)
                return index
    return None

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 12345
s.bind((host, port))

while True:
    print("\nServer is listening...")
    data, address = s.recvfrom(1024) #4096
    print(data)
    print(address)
    print("\n Server received: ", data.decode('utf-8'), "\n")

    data = data.decode('utf-8')
    comm = json.loads(data)
    print(comm)

    if comm["command"] == 'join':
        #s.connect((host, port))
        #output = "Connection to the Message Board Server is successful!"
        #s.sendto(output.encode('utf-8'), address)
        data.replace("'", '"')
        s.sendto(data.encode('utf-8'), address)
        
    elif comm["command"] == "leave": 
        indexAddress = findClientIndex(address)
        if indexAddress != None:
            clients.pop(indexAddress)           
        #command = json.dumps(leave())
        data.replace("'", '"')
        s.sendto(data.encode('utf-8'), address)
                     
    elif comm["command"] == "register":
        temp = list()
        temp.append(comm["handle"])
        temp.append(address) #address of user
        print(temp)
        clients.append(temp)
        print(clients)
        #converts to json and sends the completion of command to client
        data.replace("'", '"')
        #command = json.dumps(register(data))
        #s.sendto(command.encode('utf-8'), address)
  
        for c in clients:
            print(c[0])
            sendTo = c[1]
            s.sendto(data.encode('utf-8'), sendTo)
        print("Done registering")

    elif comm["command"] == 'all':
        data.replace("'", '"')
        username = findPerson(address)
        withHandle = username + ": " + comm["message"]
        sendAll = {"command": "all", "message": withHandle}
        ctr = 1
        for c in clients:
            print(c[0])
            sendTo = c[1]
            s.sendto(sendAll.encode('utf-8'), sendTo)
            print("Sent to " + str(ctr))
            ctr += 1
        print("Done sending to all")
    elif comm["command"] == "msg":
        data.replace("'", '"')
        print(data)
        senderName = findPerson(address)
        sender = json.dumps(fromSender(comm["message"], senderName))
        sender.replace("'", '"')
        se = json.loads(sender)
        print("Sender: " + se["handle"])

        s.sendto(data.encode('utf-8'), findAddress(senderName)) #receiver sees that message is from sender
        s.sendto(sender.encode('utf-8'), findAddress(comm["handle"]))  #sender sees that message is sent to receiver

    