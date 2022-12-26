import socket
import json

global clients
clients = list()


def sendToAll(data, name):
    message = " ".join(data[1:])
    withHandle = name + ": " + message
    print("Message: " + withHandle)
    send = {"command": "all", "message": withHandle}
    return send

def fromSender(message, name): #sets handle as person who sent the message
    withHandle = "[To " + name +  "]: " + message
    send = {"command": "msg", "handle": name, "message": withHandle}
    return send

def findPersonByName(handle):
    global clients
    for c in clients:
        if c[0] == handle:
            name = c[0]
            return name

def findPerson(address): #find person's name based on address
    global clients
    find_ip = address[0]
    find_port = address[1]
    name = "None"
    for c in clients:
        if c[1] == address:
            name = c[0]
            return name
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

def handleExists(handle):
    for c in clients:
        if c[0] == handle:
            return True
    return False


# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.1'
port = 12345
s.bind((host, port))
clients = list()

while True:
    print("\nServer is listening...")
    data, address = s.recvfrom(1024) #4096
    print("Server received: ", data.decode('utf-8'), "\n")

    data = data.decode('utf-8')
    comm = json.loads(data)

    if comm["command"] == 'join':
        data.replace("'", '"')
        s.sendto(data.encode('utf-8'), address)
        
    elif comm["command"] == "leave": 
        indexAddress = findClientIndex(address)
        if indexAddress != None:
            clients.pop(indexAddress)           
        data.replace("'", '"')
        s.sendto(data.encode('utf-8'), address)
        
    elif comm["command"] == "register":
        temp = list()
        temp.append(comm["handle"])
        temp.append(address) #address of user
        print(temp)

        if handleExists(comm["handle"]):
            json_error = {"command":"error", "message":"Error: Registration failed. Handle or alias already exists."}
            error = json.dumps(json_error)
            s.sendto(error.encode('utf-8'), address)
        
        else:
            clients.append(temp)
            print(clients)
            #converts to json and sends the completion of command to client
            data.replace("'", '"')
            for c in clients:
                print(c[0])
                sendTo = c[1]
                s.sendto(data.encode('utf-8'), sendTo)
            print("Registered new user")

    elif comm["command"] == 'all':
        sender = findPerson(address)
        withHandle = sender + ": " + comm["message"]
        print(withHandle)
        send = {"command": "all", "message": withHandle}
        send_all = json.dumps(send)
        #data.replace("'", '"')
        ctr = 1
        for c in clients:
            print(c[0])
            sendTo = c[1]
            s.sendto(send_all.encode('utf-8'), sendTo)
            print("Sent to " + str(ctr))
            ctr += 1
        print("Done sending to all")

    elif comm["command"] == "msg":
        print(clients)
        if handleExists(comm["handle"]) == False:
            json_error = {"command":"error", "message": "Error: Handle or alias not found."}
            error = json.dumps(json_error)
            s.sendto(error.encode('utf-8'), address)

        else:
            #data.replace("'", '"')
            print(data)
            senderName = findPerson(address)
            sender = json.dumps(fromSender(comm["message"], comm["handle"]))
            #sender.replace("'", '"')
            #se = json.loads(sender)

            receiverMsg = "[From " + findPerson(address) + "]: " + comm["message"]
            fromReceiver = {"command":"msg", "message": receiverMsg}
            receiver = json.dumps(fromReceiver)

            data.replace("'", '"')
            s.sendto(sender.encode('utf-8'), findAddress(senderName)) #receiver sees that message is from sender
            s.sendto(receiver.encode('utf-8'), findAddress(comm["handle"]))  #sender sees that message is sent to receiver
    elif comm["command"] == "error":
        data.replace("'", '"')
        s.sendto(data.encode('utf-8'), address)