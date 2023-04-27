import socket
import pickle
import pygame
from pygame.locals import *
from json import load
from time import perf_counter
from sys import exit

from src.world import World
from src.player import Player
from src.gui import Gui


global seconds, tick, display, temp, players, current_id

### Création des constantes à partir du fichier config.json

# Charge les données du fichier config grâce à la librairie json
with open("config.json") as f:
    config: dict = load(f)

# Définition des constantes à partir du fichier config
WIDTH = config["dimensions"]["width"]
HEIGHT = config["dimensions"]["height"]
FPS = config["fps"]
TITLE = config["title"]
X_CENTER, Y_CENTER = CENTER = (WIDTH // 2, HEIGHT // 2)

players = {}
current_id = -1


def handle_events():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            # Activer l'écran de débogage, échange la valeur booléenne
            if event.key == K_F3:
                gui.debug = not gui.debug

            elif event.key == K_a:
                # Position actuelle du joueur
                x, y = player.pos

                # Position fixée du joueur
                x_pos_fixed = world.center + round(x - int(x))
                y_pos_fixed = world.center + round(y - int(y))

                # Data aux coordonnées fixées
                pos = world.coords[y_pos_fixed][x_pos_fixed]

                # Si aux coordonnées fixées il y a un ingrédient
                if (
                    bool(round(pos[2]))  # S'il y a une végétation
                    # Si ce n'est pas de l'eau
                    and not pos[3] > world.water_level
                    and int(str(pos[2])[-2:])
                    in world.ingredients_range  # Si c'est un ingrédient
                    and world.vegetation_data[
                        int(x + x_pos_fixed),
                        int(y + y_pos_fixed),
                    ]  # S'il n'a pas été ramassé
                ):
                    # Récupérer l'ingrédient
                    gui.mixer.pok.play()
                    world.vegetation_data[
                        int(x + x_pos_fixed),
                        int(y + y_pos_fixed),
                    ] = False
                    ingredient = world.ingredients_list[
                        int(str(pos[2])[-2:]) - world.ingredients_range[0]
                    ]
                    if ingredient in player.inventory:
                        player.inventory[ingredient] += 1
                    else:
                        player.inventory[ingredient] = 1
            return "get"

        # Fermeture du jeu
        elif event.type == QUIT:
            return "quit"


def render():
    world.update(int(player.pos.x), int(player.pos.y))

    # Récupérer et afficher les sprites
    for sprite in world.get_sprites(player, players, tick):
        display.blit(sprite[0], (sprite[1], sprite[2]))

    # Dessiner l'interface graphique
    gui.draw()

    # Dessiner l'écran de débogage
    if gui.debug:
        gui.draw_debug(tick, seconds, clock.get_fps())

    # Dessiner le fondu
    if gui.fade.active:
        gui.fade.draw(screen)

    if gui.photo_fade.active:
        gui.photo_fade.draw(screen)

    pygame.display.flip()


if __name__ == "__main__":
    # Initialisation, définition du titre et des dimensions de la fenêtre
    pygame.init()
    pygame.display.set_caption(TITLE)  # "Spicy Journey"
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # (1280, 700)
    display = pygame.Surface(CENTER)  # (640, 350)
    clock = pygame.time.Clock()
    seconds: float = 0
    tick: int = 0

    SERVER_ADDR = "ulysses.ddns.net"
    SERVER_PORT = 9595

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.connect((SERVER_ADDR, SERVER_PORT))
    except socket.error as e:
        print("Failed to connect to server :")
        print(e)
        exit()
    
    current_id = int(server.recv(4).decode())
    name = input("Entrez votre pseudo : ")
    server.send(name.encode())
    response = server.recv(4).decode()
    while response == "False":
        name = input("Entrez votre pseudo : ")
        server.send(name.encode())
        response = server.recv(4).decode()

    # Création du monde
    world = World(WIDTH, HEIGHT, int(server.recv(10).decode()))
    print("Seed : %s" % world.seed)
    print("Spawn : %s" % str(world.spawn))

    # Création du personnage
    player = Player(world)

    server.send((str(world.spawn[0]) + " " + str(world.spawn[1])).encode())
    server.send(("get " + str(player.frame_index) +
                " " + player.status + player.idle).encode())
    players = pickle.loads(server.recv(1024))

    # Création du GUI (Graphical User Interface)
    gui = Gui(WIDTH, HEIGHT, screen, display, player, world)

    # Démarrage du jeu

    run = True
    while run:
        start = perf_counter()
        data = handle_events()  # Gestion des pressions sur les boutons
        if not data:
            data = "get"
        player.update()  # Gère l'animation et les mouvements du joueur
        player.frame_index = player.frame_index % len(world.player[player.status + player.idle])
        
        server.send((data + " " + str(player.frame_index) +
                    " " + player.status + player.idle).encode())
        if data == "quit":
            response = server.recv(2).decode()
            if response == "ok":
                run = False
        elif data == "get":
            players = pickle.loads(server.recv(1024))

        render()  # Effectue les calculs et dessine l'écran

        clock.tick(FPS)  # Limite les fps à la valeur inscrite dans les configs

        tick += 1  # Tick est la valeur représentative du temps en jeu
        seconds += perf_counter() - start  # Seconds est le temps passé en jeu
    
    pygame.quit()
    exit()
