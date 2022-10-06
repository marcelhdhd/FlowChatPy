import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # defines type of socket

host = "localhost"                                                        # set this to receipiants address (from Core?)
port = 8000                                                               # port to send to (anything > 1023 is fine)

my_socket.connect((host, port))                                           # connects to previously specified receiver
my_socket.send("hello".encode())                                          # fill Text with User Input from GUImanager (sends encoded message)