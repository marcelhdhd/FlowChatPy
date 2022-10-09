import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # defines type of socket

PORT = 8000                                                     # port to listen on (anything > 1023 is fine)
ADDRESS = "0.0.0.0"                                             # get ADDRESS from Core after establishing a connection from other Flowchat Application
my_socket.bind((ADDRESS, PORT))

my_socket.listen()                                              # listens for incoming connections (may be obsolete depending on implementation of TCP)
client, client_adress = my_socket.accept()                      # accept returns a tuple containing IP and Port used for incoming connection

message = client.recv(1024)                                     # receives byte object
print(message.decode)                                           # decodes received byte object into string

def listener                                                    # TBC