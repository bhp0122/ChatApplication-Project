import socket
import threading


BUFF_SIZE = 1024
PORT = 9999
IP = '127.0.0.1'  # localhost


# receive any messages and display them
def receive_display_message():
    while True: # loop to keep checking for
        message_rcd = client_socket.recv(BUFF_SIZE).decode('utf-8')
        if message_rcd:
            if message_rcd not in ['Receiver', 'Message']: # messages is this list should not be printed
                print(f'message alert: {message_rcd}\n')  # prints message from server
            else:
                handle_message(message_rcd)

# displays instructions for the user on what to enter 
def handle_message(m):
    if m == 'Receiver':
        print("Who would you like to send a message to? ") 
    elif m == 'Message':
        print("Enter message ")


if __name__ == "__main__":

    # create the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Client socket created")

    client_socket.connect((IP, PORT))
    print(f"Client now connected to server")  # prints the socket information, may remove


    # get name from user and send it to the server
    if client_socket.recv(1024).decode('utf-8') == 'Name':
        name = input('Please enter your name --> ')
        client_socket.send(name.encode('utf-8'))

    ''' this thread simultaneously runs the receive_display_message function to display a certain message based on the message received from the server'''
    receiving_thread = threading.Thread(target=receive_display_message)
    receiving_thread.start()

    message = ''
    
    print('Enter "change" at any to change the receiver') # client can enter 'change' to enter a new username of the receiver
    
    # continue to take input until user enters ".exit"
    while True:

        print("If you do not see the 'Enter message' instruction, enter a character.") # bug in the code, can enter character or string
        message = input('--> \n')
        # print("after getting input")
        client_socket.send(message.encode('utf-8'))

        # in server code, can delete
        # if message == '.exit':
        #     client_socket.close()  # close the chat if client enters ".exit"
        #     break
    
