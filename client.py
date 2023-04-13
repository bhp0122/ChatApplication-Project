import socket
import threading
import sys

BUFF_SIZE = 1024
PORT = 9999
IP = '127.0.0.1'  # localhost

running = True

# receive any messages and display them
def receive_display_message(running):
    while True:
        message_rcd = client_socket.recv(BUFF_SIZE).decode('utf-8')
        if message_rcd:
            if message_rcd not in ['RCVR', 'RCVR DNE', 'MSG', '.exit', 'DISCONNECTING']:
                print(f'{message_rcd}\n')
                client_socket.send('x'.encode('utf-8'))
            else:
                handle_message(message_rcd)



def handle_message(m):
    if m == 'RCVR':
        print("Who would you like to send a message to? ")
        return True
    elif m == 'MSG':
        print("Message: ")
        return True
    elif m == 'DISCONNECTING':
        print('You are disconnecting.')
        sys.exit()

   
if __name__ == "__main__":

    # create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client socket created")

    client_socket.connect((IP, PORT))
    print(f"Client now connected to server")

    # get username from user
    if client_socket.recv(1024).decode('ascii') == 'NAME':
        name = input('Name --> ')
        client_socket.send(name.encode('utf-8'))
        print('Enter ".exit" to exit.')
        print('Enter "change" to switch who you would like to send a message to.')
    
    # continue to take input until user enters ".exit"
    message = ''

    receiving_thread = threading.Thread(target=receive_display_message, args=[running, ])
    receiving_thread.start()

    take_input = True
    while True:
        if take_input:
            message = input(' \n')
            take_input = False
        else:
            take_input = True
            client_socket.send(''.encode('utf-8'))
            continue

        client_socket.send(message.encode('utf-8'))

    


    
