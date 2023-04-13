import socket
import threading
import random
import time

print('Server is starting...', end=' ')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# AF_INET: designates type of address can communicate: in this case IPv4
# SOCK_STREAM: defines a TCP socket

server.bind(('127.0.0.1', 9999))
# Listens for incoming requests

server.listen()
print('Server is listening...')
# Accepts the incoming requests

connected_clients = []
# Keeps track of all connected clients

usernames = []


# Keeps track of the user's nicknames


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

        usernames.append(nickname)
        # Adds connected client's nickname

        connected_clients.append(client_socket)
        # adds the client's connection to the list which consists of the socket and address

        waiting_for_clients_thread = threading.Thread(target=waiting_for_clients, args=(client_socket,))
        waiting_for_clients_thread.start()
        # if there is less than one client avaiable, the client is to wait for more clients


def waiting_for_clients(client_socket):
    # "Middle Man": If there are no other clients besides one, the client waits.
    # Once another client is connected, it starts the process of sending messages.

    if len(connected_clients) <= 1:
        client_socket.send('\nWaiting for new clients...'.encode('ascii'))

    while len(connected_clients) <= 1:
        time.sleep(10)
        client_socket.send('Waiting for new clients...'.encode('ascii'))

    broadcast('\nConnected Clients: {}'.format(usernames))
    # Sends to newly connected client that they are connected to the server
    # .encode() necessary because sockets only send bytes between each other therefore just a string would not be accepted

    handle_thread = threading.Thread(target=handle, args=(client_socket,))
    handle_thread.start()
    # Begin sending and receiving messages


def handle(client_socket):
    # Receives the message by the user and sends it to other users
    rcvr_check = None
    msg = None

    while True:
        # thinking of splitting this into two functions: getting_rcvr() and sending_msg()

        while True:
            # Receives who the client wants to send a message to
            client_socket.send('RCVR'.encode('ascii'))
            rcvr_check = client_socket.recv(1024).decode('ascii')

            if rcvr_check == '.exit':
                # If the client chooses to disconnect
                exiting(client_socket)
                return
            if rcvr_check == 'x':
                continue
            while rcvr_check == 'change' or rcvr_check == '':
                # if the client wishes to change who they are talking to
                client_socket.send('RCVR'.encode('ascii'))
                rcvr_check = client_socket.recv(1024).decode('ascii')

            while rcvr_check not in usernames:
                client_socket.send('RCVR DNE'.encode('ascii'))
                rcvr_check = client_socket.recv(1024).decode('ascii')
            break

        while True:
            # Receives the message the client wants to send
            client_socket.send('MSG'.encode('ascii'))
            msg = client_socket.recv(1024).decode('ascii')

            if msg == '.exit':
                # If the client chooses to disconnect
                exiting(client_socket)
                return
            elif msg == 'change':
                break
            elif msg == 'x':
                continue
            else:
                send(msg, rcvr_check, client_socket)


def exiting(client_socket):
    clients_index = connected_clients.index(client_socket)
    nickname = usernames[clients_index]

    client_socket.send('DISCONNECTING'.encode('ascii'))
    client_socket.close()

    connected_clients.remove(client_socket)

    broadcast('{} has left.'.format(nickname))
    print(f"{nickname} has left. ")

    usernames.remove(nickname)

    list_of_clients = {str(i) for i in usernames}
    broadcast('Connected Clients: {}'.format(list_of_clients))
    return


def send(msg, rcvr, client_socket):
    # sends the message to the desired person
    rcvrs_index = usernames.index(rcvr)
    rcvrs_socket = connected_clients[rcvrs_index]

    sndrs_index = connected_clients.index(client_socket)
    sndrs_username = usernames[sndrs_index]

    rcvrs_socket.send("From {}: {}".format(sndrs_username, msg).encode('ascii'))


def broadcast(message):
    # sends the message to everyone
    for c in connected_clients:
        c.send(message.encode('ascii'))


receive()
