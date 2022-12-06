import socket
import json

def commandlist():
    print("Command List")
    print("1. Connect to the server application: /join <server_ip_add> <port>")
    print("2. Disconnect to the server application: /leave")
    print("3. Register a unique handle or alias: /register <handle>")
    print("4. Send message to all: /all <message>")
    print("5. Send direct message to a single handle: /msg <handle> <message>")
    print("6. Request command help to output all Input Syntax commands for references: /?")

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

# Let's send data through UDP protocol
while True:
    command = input("")
    all_words = command.split()
    if command == "/leave":
        break
    elif command == "/?":
        commandlist()
    elif len(all_words) == 2 and all_words[0] == "/register":
        s.send(command.encode())
        x = s.recv(4096)
        x = x.decode('utf-8')
        x.replace("'", '"')
        command = json.loads(x)
        print("Welcome " + command["handle"])
    """ 
    elif len(all_words) >= 2 and all_words[0] == "/all":
        message = " ".join(all_words[1:])
        print(message)
        s.send(message.encode())
    """
    
    """
    else: 
        send_data = input("Type some text to send =>");
        s.sendto(send_data.encode('utf-8'), (host, port))
        print("\n\n 1. Client Sent : ", send_data, "\n\n")
        data, address = s.recvfrom(4096)
        print("\n\n 2. Client received : ", data.decode('utf-8'), "\n\n")
    """

# close the socket
s.close()
print("Connection closed. Thank you!")
