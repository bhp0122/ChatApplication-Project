import socket
import threading
import random

host = '127.0.0.1'
port = 9999

print('Server starting...')
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print("Server listening...")

clients = []

def send(message, connection):
    for client in clients:
        connection.send()



def recieve_requests():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))
        
        client.send('NAME'.encode('ascii'))
        c = client.recv(1024).decode('ascii')
        
        if c == '.exit':
            client.close()
        else:            
            name = f'{c}{random.randint(0,9)}'
            clients.append(f'{name}')
            print('{} has joined'.format(name))

        client.send('Connected to server.'.encode('ascii'))
        
        thread = threading.Thread(target = handle_messages, args=(clients, ) )
        thread.start()


def handle_messages(client):
    while True:
        try:
            message = client.recv(1024)

            if message == '.exit':
                client.close()

            send(message, client)
        except:
            client.close()

recieve_requests()


