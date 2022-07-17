import socket
from  threading import Thread

IP_ADDRESS = '127.0.0.1'
PORT = 8080
SERVER = None
clients = {}

def acceptConnections():
    global SERVER
    global clients

    while True:
        client, addr = SERVER.accept()
        client_name = client.recv(4096).decode().lower()
        clients[client_name] = {
            "client":client,
            "address":addr,
            "connected_with":"",
            "file_name":"",
            "file_size":4096
        }
        print(f"Connection Estabilished With {client_name}: {addr}")

        thread = Thread(target=handleClient , args = (client,client_name))
        thread.start()

def handleShowList(client):
    global clients
    counter = 0

    for c in clients:
        counter+=1
        client_address = clients[c]["address"][0]
        connected_with = clients[c]["connected_with"]
        message = ""

        if(connected_with):
            message=f"{counter},{c},{client_address},connected with {connected_with} , tiul , \n"
        else:
            message=f"{counter},{c},{client_address}, Available , tiul , \n"
        
        client.send(message.encode())
        time.sleep(1)


def handleMessges(client, message, client_name):
    if(message == 'show list'):
        handleShowList(client)

def handleClient(client, client_name):
    global clients
    global BUFFER_SIZE
    global SERVER

    # Sending welcome message
    banner1 = "Welcome, You are now connected to Server!\nClick on Refresh to see all available users.\nSelect the user and click on Connect to start chatting."
    client.send(banner1.encode())

    while True:
        try:
            BUFFER_SIZE = clients[client_name]["file_size"]
            chunk = client.recv(BUFFER_SIZE)
            message = chunk.decode().strip().lower()
            if(message):
                handleMessges(client, message, client_name)
            else:
                removeClient(client_name)
        except:
            pass

def setup():
    print("\n\t\t\t\t\t\tIP MESSENGER\n")

    global PORT
    global IP_ADDRESS
    global SERVER


    SERVER  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()

setup_thread = Thread(target=setup)
setup_thread.start()