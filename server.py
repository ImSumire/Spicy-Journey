"""
Doc
"""

#  ______  ______  ______  __   ________  ______
# /\  ___\/\  ___\/\  __ \/\ \ / /\  ___\/\  __ \
# \ \___  \ \  __\\ \  __<\ \ \'/\ \  __\\ \  __<
#  \/\_____\ \_____\ \_\ \_\ \__| \ \_____\ \_\ \_\
#   \/_____/\/_____/\/_/ /_/\/_/   \/_____/\/_/ /_/
#


import pickle
import socket
from random import randint
from threading import Thread
from traceback import print_exc


# pylint: disable=invalid-name
# pylint: disable=broad-except

# Initialisation de la socket du serveur
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Initialisation des constantes pour la connextion du serveur
SERVER_ADDR = "192.168.1.44"
SERVER_PORT = 9595

# Connection du serveur
server.bind((SERVER_ADDR, SERVER_PORT))

server.listen(2)
print("Server online with address : ulysses.ddns.net, listening on port :", SERVER_PORT)

# Initialisation des variables du jeu
players = {}
id_count = 1
SEED = randint(-10e4, 10e4)

print("Seed : %s" % SEED)


def name_check(_name):
    """
    Cette  fonction  vérifie  si  le pseudo  du joueur  est  valide,  voici  les
    conditions :
    - Est entre 2 et 15 de longueur
    - N'est pas rempli d'espaces
    - N'existe pas dans la liste des joueurs
    """
    if not 2 <= len(_name) <= 15:
        return False
    if _name.isspace():
        return False
    if any(_name in players[id] for id in players):
        return False
    return True


def threaded_client(conn, current_id, _players):
    """
    Cette fonction  gère toutes  les fonctionnalités  d'un  joueur en  ligne  en
    allouant un thread.
    """
    conn.send(str(current_id).encode())

    name = ""
    while name == "":
        name = conn.recv(20).decode()
        if name_check(name):
            conn.send("False".encode())
            name = ""
        else:
            conn.send("True".encode())
    print(name + " just joined the game !")

    conn.send(str(SEED).encode())
    pos = conn.recv(20).decode().split(" ")
    pos = (float(pos[0]), float(pos[1]))
    print(name + " just spawned at coords :", pos)
    _players[current_id] = [name, pos, ("down_idle", 0)]

    while True:
        try:
            data = conn.recv(200).decode().split(" ")

            status = data.pop()
            frame_index = float(data.pop())
            received_quit = data.pop()
            _players[current_id][2] = (status, frame_index)

            if received_quit == "True":
                response = "ok".encode()
                return

            if data[0] == "get":
                response = pickle.dumps(_players)
            elif data[0] == "move":
                _players[current_id][1] = (float(data[1]), float(data[2]))
                response = pickle.dumps(_players)

            conn.send(response)
        except Exception:
            print("----- Exception for " + name + " -----")
            print_exc()
            print("-" * (26 + len(name)))
            return

    del _players[current_id]

    print(name, "disconnected.")


if __name__ == "__main__":
    while True:
        host, addr = server.accept()
        print("Connected to :", addr)

        client = Thread(target=threaded_client, args=(host, id_count, players))
        client.start()
        id_count += 1
