import socket
import threading
import random
import time

host = '127.0.0.1'
port = 9999

print('Server starting...', end='')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET: designates type of address can communicate: in this case IPv4
# SOCK_STREAM: defines a TCP socket

server.bind((host, port))
# Listens for incoming requests

server.listen()
print('Server listening...')
# Accepts the incoming requests

connected_clients = []
# Keeps track of all connected clients

usernames = []
# Keeps track of the user's nicknames


def accepting_requests():
    # Accepts incoming requests
    while True:
        client_connection, address = server.accept()
        # Connects to the client side where it is defined as .connect()

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

        usernames.append(nickname)
        # Adds connected client

        connected_clients.append(client_connection)
        # adds the client's connection to the list

        handle_thread = threading.Thread(target=handle, args=(client_connection,))
        handle_thread.start()
    

def handle(client_connection):
    # "Middle Man": If there are no other clients besides one, the client waits. 
    # Once another client is connected, it starts the process of sending messages.

    while len(connected_clients) <= 1:
        client_connection.send('Waiting for new clients...'.encode('ascii'))
        time.sleep(10)


    broadcast('Connected Clients: {}'.format(usernames)) 
    # Notfies all connected clients of the all of the clients available

    forwarding_thread = threading.Thread(target=forwarding, args=(client_connection,))
    forwarding_thread.start()


def broadcast(message):
    # sends the message to everyone
    for c in connected_clients:
        c.send(message.encode('ascii'))


def send(message, receiver, client_connection):
    # sends the message to the desired person
    receivers_index = usernames.index(receiver)
    receiver_connection = connected_clients[receivers_index]

    senders_index = connected_clients.index(client_connection)
    senders_name = usernames[senders_index]

    receiver_connection.send("From {}: {}".format(senders_name, message).encode('ascii'))


def forwarding(client_connection):
    # Receives the message by the user and sends it to other users
    receiver = None
    message = '' 

    while True:
        if message == 'change' or receiver is None: # Precious: client can enter 'change' to switch receivers
            client_connection.send('Receiver'.encode('ascii'))
            receiver = client_connection.recv(1024).decode('ascii')
            # needs to know who to direct the message to

        elif message == '.exit':
        # if the client decides to disconnect
            client_index = connected_clients.index(client_connection)
            # removes client's socket from connected list

            nickname = usernames[client_index]
            
            client_connection.send('You have disconnected.'.encode('ascii'))

            client_connection.close()
            # close the disconnecting clients socket

            connected_clients.remove(client_connection)
            # removes the client's connection for list

            broadcast('{} has left.'.format(nickname))
            # inform other clients that a client has left

            print(f"{usernames[client_index]} has left.")
            # Let's server know that a client has left.

            usernames.remove(nickname)
            # removes user's nickname in the list 

            list_of_clients = {str(i) for i in usernames}
            broadcast('Connected Clients: {}'.format(list_of_clients))
            # informs users of currently connected clients
            break

        client_connection.send('Message'.encode('ascii'))

        message = client_connection.recv(1024).decode('ascii')
        # Receives message of up to 1024 bytes

        send(message, receiver, client_connection)
        # forwards message to desired person

        message = client_connection.recv(1024).decode('ascii') 


accepting_requests_thread = threading.Thread(target=accepting_requests)
accepting_requests_thread.start()
# Continues to accept incoming connections even if there is only one client waiting for another client to join.
