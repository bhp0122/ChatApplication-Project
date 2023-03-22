# This is the code for the client side
import socket

BUFF_SIZE = 1024
PORT = 9999
IP = '127.0.0.1'
# create the client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Client socket created")

# connect socket to address (server)
# host = socket.gethostname() # hello-2.uom.memphis.edu
# ip = socket.gethostbyname(host)

client_socket.connect((IP, PORT))
print(f"Client {client_socket} now connected to server") # prints the socket information, may remove

# create and send message
message = input("Start chatting: ")
while message != ".exit":
    client_socket.sendall(message.encode('utf-8'))

    # receive any messages and display them
    message_rcd = client_socket.recv(BUFF_SIZE).decode('utf-8')
    print(message_rcd)
    message = input("--> ") # take input for next message

client_socket.close() # close the chat if client enters ".exit"


