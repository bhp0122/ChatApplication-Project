import socket

BUFF_SIZE = 1024
PORT = 9999
IP = '127.0.0.1'

# receive any messages and display them
def receive_display_message():
    message_rcd = client_socket.recv(BUFF_SIZE).decode('utf-8')
    if not message_rcd:
        return 0
    else:
        print(message_rcd)
        return 1


if __name__ == "__main__":
    # create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client socket created")

    client_socket.connect((IP, PORT))
    print(f"Client {client_socket} now connected to server") # prints the socket information, may remove

    # create and send message
    message = ''
    # get username from user

    print("Enter your username: \n")
    # continue to take input until user enters ".exit"

    while message != ".exit":
        message = input("--> ") # first time gets username
        client_socket.send(message.encode('utf-8'))
        if receive_display_message() == 0:
            message = input("--> ") # takes input for next message

    client_socket.close() # close the chat if client enters ".exit"

