import socket
import threading
import sys

BUFF_SIZE = 1024
PORT = 9999
IP = '127.0.0.1'  # localhost

running = True
stop = False


# receive any messages and display them
def receive_display_message(running):
    while True:
        message_rcd = client_socket.recv(BUFF_SIZE).decode('utf-8')
        if message_rcd:
            if not any(i in message_rcd for i in ['RCVR', 'RCVR DNE', 'MSG', '.exit', 'DISCONNECTING']) :
                print(f'{message_rcd}\n')
                client_socket.send('x'.encode('utf-8'))
            else:
                handle_message(message_rcd)

# display the appropriate message depending on the message from the server
def handle_message(m):
    if 'RCVR' in m:
        print("Who would you like to send a message to? ")
        return True
    elif 'MSG' in m:
        print("Message: ")
        return True
    elif m == 'DISCONNECTING':
        print('You are disconnecting.')
        global stop
        stop = True
        exit()


if __name__ == "__main__":

    # create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client socket created")

    # connect client to server
    client_socket.connect((IP, PORT))
    print(f"Client now connected to server")

    # get username from user
    if client_socket.recv(1024).decode('ascii') == 'NAME':
        name = input('Name --> ')
        client_socket.send(name.encode('utf-8'))
        print('Enter ".exit" to exit.')
        print('Enter "change" to switch who you would like to send a message to.')

    message = ''

    # thread to check for message from server
    receiving_thread = threading.Thread(target=receive_display_message, args=[running, ])
    receiving_thread.start()

    take_input = True
    # to continue to take input from the user until stop is True
    while not stop:
        if take_input:
            message = input(' \n')
            take_input = False
        else:
            take_input = True
            client_socket.send(''.encode('utf-8')) # send the message to the server
            continue

        client_socket.send(message.encode('utf-8'))



