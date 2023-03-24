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
    # Bhumi: I don't think the client will need this. 
   

    # create and send message
    message = ''
    # get username from user

    print("Enter your username: \n")
    # continue to take input until user enters ".exit"
    
    '''
    Bhumi: Since the server needs the user's username, it will have to receive it from the person so it can let everyone else know so anyone can send a message 
    
    Ex. if client_socket.recv(1024).decode('ascii') == 'Name':
            name = input('Please enter your name --> ')
            client_socket.send(name.encode('ascii'))
    '''
    
    
    while message != ".exit":
        '''
        Bhumi: Before the client is able to read input, the server needs to let the user know its connected
        and what clients are already connected. The server also needs to know who the message is going to be for.
        
        Ex. messsage_rcv = client_socket.recv(1024).decode('ascii')
        
            if message_received == 'Receiver':
                receiver = input('Who would you like to send this message to? ')
                client_socket.send(receiver.encode('ascii'))
            if message_received == 'Message':
                message = input(f'To {receiver}: ')
                client_socket.send(message.encode('ascii'))
            elif message_received != 'Receiver' and message_received != 'Message':
                print(message_received)
        
        This is what I used. The above worked to some extent, but it was still buggy.   
        '''
        
        message = input("--> ") # first time gets username
        client_socket.send(message.encode('utf-8'))
        if receive_display_message() == 0:
            message = input("--> ") # takes input for next message

    client_socket.close() # close the chat if client enters ".exit"

