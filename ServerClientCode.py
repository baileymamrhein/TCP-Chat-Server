# %%
# Importing two packages: socket for network connection and
  # threading for multitasking
import socket
import threading

host = '127.0.0.1'
port = 55555

# Starting the server
# AF_INET = internet socket =/ unix socket
# SOCK_STREAM = TCP =/ UDP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

# Create storage values for two clients to interact with the chat
clients = []
nicknames = []

# Message broadcasting
def broadcast(message):
    for clients in clients:
        clients.send(message)

# Responsible for handing messages from clients. Each time
   # a client connects, the loop begins and looks for messages
   # to broadcast to all connected clients
def handle(client):
    while True:
        try: 
            # Broadcasts the messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # When the loop errors out, it will broadcast that
               # said client has left and remove their nickname
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Now, lets create the loop that will allow the server to 
   # continuously look for clients- listening function
def recieve():
    while True:
        # Accepting the connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Adding nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        #Print/broadcast nicknames
        print ("nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Note: the encode & ASCII functions are needed to translate
   # bytes into strings

# %%
# Now, lets create the clients to use the server
import socket
import threading

# Ask the client to choose their nickname [screen name]
nickname = input("Choose your nickname: ")

# Connect to the chat server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Function 1: message receiving
def receive():
    while True:
        try: 
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
                # Close connection if error occurs
                print("An error occured.")
                client.close
                break
# Function 2: message sending
def write():
    while True:
        message = '{}: {}'.format(nickname, input(''))
        client.send(message.encode('ascii'))

# Function 3: thread them together
receive_thread = threading.Thread(target=recieve)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()


