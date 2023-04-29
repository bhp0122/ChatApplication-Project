import socket
import threading
import sys
import ssl

BUFF_SIZE = 1024
PORT = 9999
IP = '127.0.0.1'  # localhost

# receive any messages and display them
def receive_display_message():
    while True:
        msg = wrapped_client.recv(1024).decode('ascii')
        if msg == 'DISCONNECTING':
            sys.exit()
        else:
            print(msg)


# user enters message to send
def handle_message():
    while True:
        message = input('')
        if message == '.exit':
            wrapped_client.send(message.encode('ascii'))
            sys.exit()
        else:
            wrapped_client.send(message.encode('ascii'))


if __name__ == "__main__":
    # create the context and verify the server's certificate
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_3  # uses the newest TSL version for better security
    context.load_verify_locations('server-cert.pem')

    # load the client certificate and private key
    context.load_cert_chain(certfile='client-cert.pem', keyfile='client-key.pem')

    # create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # wrap the client socket for SSL encryption
    wrapped_client = context.wrap_socket(client_socket, server_hostname=IP)

    # connect client to server
    try:
        wrapped_client.connect((IP, PORT))
        print("Client socket created")
        print(f"Client now connected to server")

        # get username from user
        msg = wrapped_client.recv(1024).decode('ascii')

        if msg == 'NAME':
            name = input('Please enter your name: ')
            while True:
                if name.isalpha() == False:
                    name = input('Invalid name. Please enter a valid name: ')
                else:
                    wrapped_client.send(name.encode('utf-8'))
                    break

        print('You can begin to enter messages.')

        # thread to check for message from server
        receive_thread = threading.Thread(target=receive_display_message)
        receive_thread.start()

        # to continue to take input from the user
        handle_thread = threading.Thread(target=handle_message)
        handle_thread.start()

    except:
        print("Could not properly connect to server. Server may be unavailable.")