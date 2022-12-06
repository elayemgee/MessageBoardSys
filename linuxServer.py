import socket
import json


def register(data):
    person = {"command": "register", "handle": data[1]}
    return person

def sendToAll(data):
    message = " ".join(data[1:])
    print("Message: " + message)
    send = {"command": "all", "message": message}
    return send

# Create a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clients = list()
connect = input("")
if connect == '{"command":"join"}':
    host = '127.0.0.1'
    port = 12345
    s.bind((host, port))
# Bind the socket to the port
""" 
server_address = (ip, port)
s.bind(server_address)
print("Do Ctrl+c to exit the program !!")
""" 

while True:
    print("####### Server is listening #######")
    data, address = s.recvfrom(4096)
    print(data)
    print(address)
    print("\n\n 2. Server received: ", data.decode('utf-8'), "\n\n")

    data = data.decode()
    data = data.split()
    if data[0] == '/register':
        temp = list()
        temp.append(data[1])
        temp.append(address)
        print(temp)
        clients.append(temp)

        print(clients)
        #converts to json and sends the completion of command to client
        command = json.dumps(register(data))
        s.sendto(command.encode('utf-8'), address)
    elif data[0] == '/all':
        command = json.dumps(sendToAll(data))
        ctr = 1
        for c in clients:
            print(c[0])
            sendTo = c[1]
            s.sendto(command.encode('utf-8'), sendTo)
            print("Sent to " + str(ctr))
            ctr += 1
        print("Done")

    

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