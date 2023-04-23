import socket
import threading
import sys

BUFF_SIZE = 1024
PORT = 9999
IP = '127.0.0.1'  # localhost

# receive any messages and display them
def receive_display_message():
    while True:
        msg = client_socket.recv(1024).decode('ascii')
        if msg == 'DISCONNECTING':
            sys.exit()
        else:
            print(msg)

# user enters message to send
def handle_message():
    while True:
        message = input('')
        if message == '.exit':
            client_socket.send(message.encode('ascii'))
            sys.exit()
        else:
            client_socket.send(message.encode('ascii'))
        

if __name__ == "__main__":
    # create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client socket created")

    # connect client to server
    client_socket.connect((IP, PORT))
    print(f"Client now connected to server")


    # get username from user
    msg = client_socket.recv(1024).decode('ascii')
    if msg == 'NAME':
        name = input('Please enter your name: ')
        client_socket.send(name.encode('utf-8'))

    print('You can not begin to enter messages.')

    # thread to check for message from server
    receive_thread = threading.Thread(target=receive_display_message)
    receive_thread.start()

    # to continue to take input from the user
    handle_thread = threading.Thread(target=handle_message)
    handle_thread.start()
