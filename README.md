# MessageBoardSys
CSNETWK

## Project Description
A Message Board System that allows clients to communicate with other clients through the server using the UDP protocol. This project uses 
Python's threading module. The project only works on MacOS.

## How to Use the System
1. Run server.py
2. Run client.py
3. Input the command '/join 127.0.0.1 12345' to join the server
4. After joining the server, one can input other commands from the list below

## Command List
1. Connect to the server application: /join <server_ip_add> <port>
2. Disconnect to the server application: /leave
3. Register a unique handle or alias: /register <handle>
4. Send message to all: /all <message>
5. Send direct message to a single handle: /msg <handle> <message> 
6. Request command help to output all Input Syntax commands for references: /?
