import socket
import threading
import random

print('Server is starting...', end=' ')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET: designates type of address can communicate: in this case IPv4
# SOCK_STREAM: defines a TCP socket

server.bind(('127.0.0.1', 9999))
# Listens for incoming requests

server.listen()
print('Server is listening...')
# Accepts the incoming requests

connected_clients = {}


def broadcast(message):
    # Sends the message to everyone
    for c in connected_clients.keys():
        c.send(message.encode('ascii'))

def receive():
    # Accepts incoming requests
    while True:
        client_socket, address = server.accept()
        # Connects to the client side where it is defined as .connect() inside the client file

        client_socket.send('NAME'.encode('ascii'))
        # .send() is only used with a connected socket ∴ uses the client socket to send
        # Asks name from the client to turn into nickname.

        name = client_socket.recv(1024).decode('ascii')
        # Receives the client's name
        nickname = f"{name}{random.randint(0, 9)}"
        # Assignes a nickname to the client: name + number

        print(f"Connected with {name} as {nickname}: {address}")
        # Shows the name and address of newly connected client only to the server

        connected_clients[client_socket] = nickname
        # Adds the client's connection to the dictionary which consists of the socket, address, and nickname

        broadcast('{} has joined.'.format(connected_clients[client_socket]))
        broadcast(' Now Connected Clients: {}'.format(list(connected_clients.values())))
        # Sends the message to everybody.

        handle_thread = threading.Thread(target=handle, args=(client_socket,))
        handle_thread.start()
        # Allows the receive function to continue to take requests, while handling exchange of messages


def send(msg, other_client, client_socket):
    # Sends message to desired person. 
    rcvr_socket = list(filter(lambda x: connected_clients[x] == other_client, connected_clients))[0]
    rcvr_socket.send("From {}: {}".format(connected_clients[client_socket], msg).encode('ascii'))
    return

def handle(client_socket):
    # Receives the message by the user and sends it to other users
    while True:
        msg = client_socket.recv(1024).decode('ascii')

        rcvr = None
        for other_client in connected_clients.values():
            if '@' + other_client in msg:
                send(msg, other_client, client_socket)
                rcvr = other_client
                break
        if msg == '.exit':
            exit(client_socket)
            return
        elif rcvr == None:
            broadcast('From {}: {}'.format(connected_clients[client_socket], msg))

def exit(client_socket):
    # Notfies everyone that a client has left, and closes the client's socket. 
    broadcast('{} has left'.format(connected_clients[client_socket]))
    print(f"{connected_clients[client_socket]} has left.")

    client_socket.send('DISCONNECTING'.encode('ascii'))
    client_socket.close()

    del connected_clients[client_socket]
    return
    
receive()
