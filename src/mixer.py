"""
Ce script  définit une classe `Mixer`  pour centraliser les sons et les musiques
et  simplifier leur utilisation.  Il   utilise  le multithreading   pour charger
rapidement les musiques et les sons.
"""

#  __    __  __  __  __  ______  ______
# /\ "-./  \/\ \/\_\_\_\/\  ___\/\  __ \
# \ \ \-./\ \ \ \/_/\_\/\ \  __\\ \  __<
#  \ \_\ \ \_\ \_\/\_\/\_\ \_____\ \_\ \_\
#   \/_/  \/_/\/_/\/_/\/_/\/_____/\/_/ /_/
#

# pylint: disable=duplicate-code
# Pour pouvoir lancer le programme avec n'importe quel fichier
if __name__ == "__main__":
    from os.path import dirname, realpath, join
    from subprocess import call
    import sys

    DIR_PATH = dirname(realpath(__file__))
    call(["python3", join(DIR_PATH, "../main.py")])

    sys.exit()

# pylint: disable=wrong-import-order
# pylint: disable=wrong-import-position
# pylint: disable=consider-using-f-string
# pylint: disable=too-many-instance-attributes

from os.path import realpath

# J'utilise le multithreading pour charger plus rapidement les musiques et sons,
# ça passe de  0.5 secondes à 0.03, ce qui est très important pour le comfort au
# démarrage.
import threading

from random import shuffle, randint
from pygame import mixer

from src.tools.memoize import memoize

mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)


class Mixer:
    """
    Cette classe a pour  but de centraliser les sons et musiques pour simplifier
    leurs utilisations.
    """
    def __init__(self):
        self.playing_music = True
        self.playing_ambient = True


        self.musics = [
            "Avril-14th",
            "Bluebird",
            "La-valse-dAmelie",
            "Last-Carnival",
            "Secret-OST",
            "Song-on-the-Beach",
        ]

        # Mélange dans l'ordre des musiques
        shuffle(self.musics)

        # Lancement de la première musique
        self.music_thread = threading.Thread(
            target=self.load_music, args=("res/music/%s.mp3" % self.musics[0],)
        )
        self.music_thread.start()

        # Ajout des autres musiques dans la queue
        self.queue_thread = threading.Thread(target=self.load_music_queue)
        self.queue_thread.start()

        # Ambience avec les oiseaux
        self.ambience_thread = threading.Thread(
            target=self.loop_sound, args=("res/sound/ambience.wav",)
        )
        self.ambience_thread.start()

        # Son de vent
        self.wind_thread = threading.Thread(
            target=self.loop_sound, args=("res/sound/wind.wav",)
        )
        self.wind_thread.start()

        self.page = [
            self.load_sound(path)
            for path in [
                "res/sound/paper/1.wav",
                "res/sound/paper/2.wav",
                "res/sound/paper/3.wav",
                "res/sound/paper/4.wav",
                "res/sound/paper/5.wav",
                "res/sound/paper/6.wav",
                "res/sound/paper/7.wav",
                "res/sound/paper/8.wav",
                "res/sound/paper/9.wav",
            ]
            if self.load_sound(path)
        ]

        # Son de pok quand un ingrédient est récolté
        self.pok = self.load_sound("res/sound/pok.wav")

        # Son de l'appareil photo
        self.photo_sound = self.load_sound("res/sound/photo.wav")

    @staticmethod
    def load_music(filename):
        """
        Charge la musique choisie, met son volume à 10% et la joue.
        """
        mixer.music.load(filename)
        mixer.music.set_volume(0.1)
        mixer.music.play(-1)

    def load_music_queue(self):
        """
        Charge le reste des musiques.
        """
        for music in self.musics[1:]:
            mixer.music.queue("res/music/%s.mp3" % music)

    @staticmethod
    def loop_sound(filename):
        """
        Créé une boucle sur le son choisie.
        """
        sound = mixer.Sound(filename)
        sound.set_volume(0.4)
        sound.play(loops=-1)

    @staticmethod
    @memoize
    def load_sound(filename):
        """
        Retourne le  son choisie avec  un volume de 40%. Nous  utilisons un  try
        pour  éviter une  erreur au  début car  certaines versions  de python ne
        veulent pas ouvrir des fichiers de musique :
        stackoverflow.com/questions/14845896/pygame-cannot-open-sound-file
        Normalement ça a été fixé mais nous le laissons au cas où...
        """
        try:
            sound = mixer.Sound(filename)
            sound.set_volume(0.4)
            return sound
        except:
            print("Unable to open file '%s'" % filename)
            return None

    @staticmethod
    def play():
        """
        Commence à jouer la musique du mixer.
        """
        mixer.music.play(-1)

    def play_ambience(self):
        """
        Réactive l'ambience.
        """
        # Ambience avec les oiseaux
        ambience_thread = threading.Thread(
            target=self.loop_sound, args=("res/sound/ambience.wav",)
        )
        ambience_thread.start()

        # Son de vent
        wind_thread = threading.Thread(
            target=self.loop_sound, args=("res/sound/wind.wav",)
        )
        wind_thread.start()

    @staticmethod
    def stop_music():
        """
        Arrête toute musique lancée.
        """
        mixer.music.stop()

    @staticmethod
    def stop_ambience():
        """
        Arrête toute ambience lancée.
        """
        mixer.stop()

    def page_sound(self):
        """
        Joue un son aléatoire de page qui tourne.
        """
        self.page[randint(0, len(self.page) - 1)].play()
