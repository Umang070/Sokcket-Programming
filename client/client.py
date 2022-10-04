import socket



def receive_message_ending_with_token(active_socket, buffer_size, eof_token):
    """
    Same implementation as in receive_message_ending_with_token() in server.py
    A helper method to receives a bytearray message of arbitrary size sent on the socket.
    This method returns the message WITHOUT the eof_token at the end of the last packet.
    :param active_socket: a socket object that is connected to the server
    :param buffer_size: the buffer size of each recv() call
    :param eof_token: a token that denotes the end of the message.
    :return: a bytearray message with the eof_token stripped from the end.
    """
    working_directory_info = bytearray()
    while True:
        recv_packet = active_socket.recv(buffer_size)
        working_directory_info.extend(recv_packet)
        if recv_packet[-10:] == eof_token:
            working_directory_info = working_directory_info[:-10]
            break
    print('Working Directory Info:', working_directory_info.decode())
    # raise NotImplementedError('Your implementation here.')


def initialize(host, port):
    """
    1) Creates a socket object and connects to the server.
    2) receives the random token (10 bytes) used to indicate end of messages.
    3) Displays the current working directory returned from the server (output of get_working_directory_info() at the server).
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param host: the ip address of the server
    :param port: the port number of the server
    :return: the created socket object
    """
    global eof_key
    global client_socket_obj
    try:
        client_socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Client Socket Successfully Created !")
    except socket.error as s_error:
        print(f"Client socket is not created due to this error : {s_error}")
    
    
    # with client_socket_obj: #if uncomment this it means only valid till client_socket_obj is available
    client_socket_obj.connect((host, port)) #connect to server 
    print('Connected to server at IP:', host, 'and Port:', port)
    eof_key = client_socket_obj.recv(1024)
    print('Handshake Done. EOF is:', eof_key.decode())
    receive_message_ending_with_token(client_socket_obj,1024,eof_key)
        


    # raise NotImplementedError('Your implementation here.')


def issue_cd(command_and_arg, client_socket, eof_token):
    """
    Sends the full cd command entered by the user to the server. The server changes its cwd accordingly and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    print("Change Directory Called ",command_and_arg)
    client_socket.sendall(command_and_arg.encode())
    # receive_message_ending_with_token(client_socket,1024, eof_token)
    


def issue_mkdir(command_and_arg, client_socket, eof_token):
    """
    Sends the full mkdir command entered by the user to the server. The server creates the sub directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    print("Create Directory Called ",command_and_arg)
    
    client_socket.sendall(command_and_arg.encode())
    # receive_message_ending_with_token(client_socket,1024, eof_token)

    


def issue_rm(command_and_arg, client_socket, eof_token):
    """
    Sends the full rm command entered by the user to the server. The server removes the file or directory and sends back
    the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    print("Remove  Directory Called ",command_and_arg)
    
    client_socket.sendall(command_and_arg.encode())
    


def issue_ul(command_and_arg, client_socket, eof_token):
    """
    Sends the full ul command entered by the user to the server. Then, it reads the file to be uploaded as binary
    and sends it to the server. The server creates the file on its end and sends back the new cwd info.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    """
    raise NotImplementedError('Your implementation here.')


def issue_dl(command_and_arg, client_socket, eof_token):
    """
    Sends the full dl command entered by the user to the server. Then, it receives the content of the file via the
    socket and re-creates the file in the local directory of the client. Finally, it receives the latest cwd info from
    the server.
    Use the helper method: receive_message_ending_with_token() to receive the message from the server.
    :param command_and_arg: full command (with argument) provided by the user.
    :param client_socket: the active client socket object.
    :param eof_token: a token to indicate the end of the message.
    :return:
    """
    raise NotImplementedError('Your implementation here.')


def main():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    # raise NotImplementedError('Your implementation here.')

    initialize(HOST,PORT)

    while True:
        # get user input
        try:
            
            print('1. Change Directory')
            print('2. Make New Directory')
            print('3. Remove Directory')
            print('4. Upload a File')
            print('5. Download a File')
            print('6. Exit')
            num = int(input('Enter your choice: '))
            
           

            
            if num == 1:
                user_dir_command = input('Enter a command for change directory : ')                
                issue_cd(user_dir_command, client_socket_obj, eof_key)
                
            elif num == 2:
                user_dir_command = input('Enter a command for new directory : ')
                issue_mkdir(user_dir_command, client_socket_obj, eof_key)
            elif num == 3:  
                user_dir_command = input('Enter a command for remove directory/file : ')
                issue_rm(user_dir_command,client_socket_obj, eof_key)

            elif num == 4:
                issue_ul()
            elif num == 5:
                issue_dl()
            elif num == 6:
                print('Connection Closed !!!')
                client_socket_obj.sendall('exit'.encode())
                client_socket_obj.close()
                break    
            

        except ValueError:
            print('Invalid Input Try Again !.')   
        # call the corresponding command function or exit


    print('Exiting the application.')


if __name__ == '__main__':
    main()