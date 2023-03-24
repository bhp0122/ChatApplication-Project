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

connected_clients = []
# Keeps track of all connected clients

usernames = []
# Keeps track of the user's nicknames 


def handle():
    # Handles all the incoming connections and establishes them
    while True:
        client_connection, address = server.accept()
        # Connects to the client side where it is defined as .connect()
        # Will remain available to listen for more connections

        client_connection.send('Name'.encode('ascii'))
        # .send() is only used with a connected socket ∴ uses the client socket to send
        # Asks name from the client to turn into nickname.

        name = client_connection.recv(1024).decode('ascii')
        # Receives the client's name

        nickname = f"{name}{random.randint(0, 9)}"
        # Assigned nickname to client: name + number

        print(f"Connected with {name} as {nickname}: {address}")
        # Shows the name and address of newly connected client only to the server

        client_connection.send('Connected to server as {}...'.format(nickname).encode('ascii'))
        # Sends to newly connected client that they are connected to the server
        # .encode() necessary because sockets only send bytes between each other therefore just a string would not be accepted

        message = '{} has joined'.format(nickname)
        broadcast(message)
        # Notifies everyone that a newly connected client has joined

        usernames.append(nickname)
        # Adds connected client

        connected_clients.append(client_connection)
        # adds the client's connection to the list

        list_of_clients = {str(i) for i in usernames}
        broadcast('\nConnected Clients: {}'.format(list_of_clients))
    
        forwarding_thread = threading.Thread(target = forwarding, args = (client_connection, ))
        forwarding_thread.start()
    
def broadcast(message):
    # sends the message to everyone
    for c in connected_clients:
        c.send(message.encode('ascii'))


def send(message, receiver):
    # sends the message to the desired person
    client_index = usernames.index(receiver)
    receiver_connection = connected_clients[client_index]
    receiver_connection.send(message.encode('ascii'))


def forwarding(client_connection):
    # Receives the message by the user and sends it to other users
    while True:
        client_connection.send('Receiver'.encode('ascii'))
        receiver = client_connection.recv(1024).decode('ascii')
        # needs to know who to direct the message to

        client_connection.send('Message'.encode('ascii'))
        message = client_connection.recv(1024).decode('ascii')
        # Receives message of up to 1024 bytes

        send(message, receiver)
        # forwards message to desired person

        if message == '.exit':
        # if the client decides to disconnect
            client_index = connected_clients.index[client_connection]
            
            client_connection.send('You have disconnected.'.encode('ascii'))
            
            # close the disconnecting clients socket
            client_connection.close()

            connected_clients.remove(client_connection)
            # removes the client's connection for list
            
            broadcast('{} has left.'.format(usernames[client_index]))
            # inform other clients that a client has left

            print(f"{usernames[client_index]} has left.")
            # Let's server know that a client has left. 

            usernames.remove(client_index)

            print(connected_clients)
            break 



handle()
