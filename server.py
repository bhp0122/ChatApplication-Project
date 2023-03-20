import socket
import threading
import random

host = '127.0.0.1'
port = 9999

print('Server starting...', end='')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET: designates type of address can communicate: in this case IPv4
# SOCK_STREAM: defines a TCP socket

server.bind((host,port))
# Listens for incoming requests

server.listen()
print('Server listening...')
# Accepts the incoming requests

clients = []
# Keeps track of all connected clients



def handle():
    # Handles all the incoming connections and establishes them
    while True:
        client, address = server.accept()
        # Connects to the client side where it is defined as .connect()
        # Will remain available to listen for more connections

        client.send('Name: '.encode('ascii'))
        # .send() is only used with a connected socket ∴ uses the client socket to send
        # Asks name from the client to turn into nickname.

        name = client.recv(1024).decode('ascii')
        # Receives the client's name

        nickname = f"{name}{random.randint(0, 9)}"
        # Assigned nickname to client: name + number

        clients.append(nickname)
        # Adds connected client

        print(f"Connected with {name} as {nickname}: {address}")
        # Shows the name and address of newly connected client only to the server


        client.send('Connected to server.'.encode('ascii'))
        # Sends to newly connected client that they are connected to the server
        # .encode() necessary because sockets only send bytes between each other therefore just a string would not be accepted

        client.send('Nickname is {}.'.format(nickname).encode('ascii'))
        # Inform client of nickname established

        message = '{} has joined'.format(nickname)
        broadcast(message.encode('ascii'))
        # Notifies everyone that a newly connected client has joined


        forwarding_thread = threading.Thread(target = forwarding, args = (client, ))
        forwarding_thread.start()
        
def broadcast(message):
    for client in clients:
        client.send(message)
        # Sends the message to every connected user

def forwarding(client_connection):
    # Receives the message by the user and sends it to other users
    while True:
        message = client_connection.recv(1024)
        # Receives message of up to 1024 bytes

        if message == '.exit':
        # if the client decides to disconnect
            client_index = clients.index(client_connection)
            client_connection.send('Leaving...'.encode('ascii'))


            broadcast('{} has left'.format(clients[client_index]).encode('ascii'))
            # inform other clients

            print(f"{clients[client_index]} has left.")
            clients.remove(client_index)
            
            # close the disconnecting clients socket
            client_connection.close()
            break

        broadcast(message)
        # Sends to all the other clients connected

handle()