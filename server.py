import socket
import pickle
from threading import Thread
from sys import exit
from random import randint


# Initialisation de la socket du serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Initialisation des constantes pour la connextion du serveur
SERVER_ADDR = "192.168.1.44"
SERVER_PORT = 9595

# Connection du serveur
try:
    server.bind((SERVER_ADDR, SERVER_PORT))
except socket.error as e:
    print("Server failed to start :")
    print(e)
    exit()

server.listen(2)
print("Server online with address : ulysses.ddns.net, listening on port :", SERVER_PORT)

global players

# Initialisation des variables du jeu
players = {}
idCount = 1
SEED = randint(-10e4, 10e4)

print("Seed : %s" % SEED)

def threaded_client(conn: socket.socket, current_id: int):
    conn.send(str(current_id).encode())

    name = ""
    while name == "":
        name = conn.recv(20).decode()
        if (not (2 <= len(name) <= 15)) or name.count(" ") == len(name) or any(name in players[id] for id in players):
            conn.send("False".encode())
            name = ""
        else:
            conn.send("True".encode())
    
    conn.send(str(SEED).encode())
    pos = conn.recv(10).decode()
    pos = (int(pos[:pos.index(" ")]), int(pos[pos.index(" ") + 1:]))

    players[current_id] = [name, pos, 0]

    run = True
    while run:
        try:
            data = conn.recv(50).decode().split(" ")

            players[current_id][2] = (data.pop(), float(data.pop()))

            if data[0] == "get":
                response = pickle.dumps(players)
            elif data[0] == "quit":
                response = "ok".encode()
                run = False
            
            conn.send(response)
        except Exception as e:
            print(e)
            run = False

    del players[current_id]

    print(name, "disconnected.")


run = True
while run:
    host, addr = server.accept()
    print("Connected to :", addr)

    client = Thread(target=threaded_client, args=(host, idCount))
    client.start()
    idCount += 1
