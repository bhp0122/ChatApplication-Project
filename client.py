import socket
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 9999))

if client_socket.recv(1024).decode('ascii') == 'NAME':
    name = input('Name --> ')
    client_socket.send(name.encode('ascii'))
    print('Enter ".exit" to exit.')
    print('Enter "change" to switch who you would like to send a message to.')

def receive_display_messages():
    while True:
        received_message = client_socket.recv(1024).decode('ascii')
        if received_message not in ['RCVR', 'RCVR DNE', 'MSG']:
            print(f"{received_message}")
        else:
            output = handle(received_message)
            if output == 0:
                return


def handle(received_message):
    rcvr = ''
    if received_message == 'RCVR':
        rcvr = input('Who would you like to send a message to? ')
        
        if rcvr == '.exit':
            client_socket.send(rcvr.encode('ascii'))
            return 0
        else:
            client_socket.send(rcvr.encode('ascii'))

    if received_message == 'MSG':
        msg = input('\nMessage: ')

        if msg == '.exit':
            client_socket.send(rcvr.encode('ascii'))
            return 0
        else:
            client_socket.send(msg.encode('ascii'))



receiving_thread = threading.Thread(target=receive_display_messages)
receiving_thread.start()
