#  __    __  __  __  __  ______  ______
# /\ "-./  \/\ \/\_\_\_\/\  ___\/\  __ \
# \ \ \-./\ \ \ \/_/\_\/\ \  __\\ \  __<
#  \ \_\ \ \_\ \_\/\_\/\_\ \_____\ \_\ \_\
#   \/_/  \/_/\/_/\/_/\/_/\/_____/\/_/ /_/
#

from random import shuffle, randint
from pygame import mixer

# J'utilise le multithreading pour charger plus rapidement les musiques et sons,
# ça passe de  0.5 secondes à 0.03, ce qui est très important pour le comfort au
# démarrage.
import threading

mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)


class Mixer:
    def __init__(self):
        self.musics = [
            "Cries and Whispers",
            "A Bittersweet Life",
            "Epilogue",
            "Holding Back Tears",
            "Last Carnival",
            "Long Long Ago",
            "路小雨",
        ]

        # Musique au début
        shuffle(self.musics)
        self.music_thread = threading.Thread(
            target=self.load_music, args=("res/music/%s.mp3" % self.musics[0],)
        )
        self.music_thread.start()

        # Ajout des autres musiques dans la queue
        self.queue_thread = threading.Thread(
            target=self.load_music_queue, args=(self.musics,)
        )
        self.queue_thread.start()

        # Ambience avec les oiseaux
        self.ambience_thread = threading.Thread(
            target=self.loop_sound, args=("res/sound/ambience.mp3",)
        )
        self.ambience_thread.start()

        # Son de vent
        self.wind_thread = threading.Thread(
            target=self.loop_sound, args=("res/sound/wind2.wav",)
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
        ]

        # Son de pok quand un ingrédient est récolté
        self.pok = mixer.Sound("res/sound/pok.wav")
        self.pok.set_volume(0.3)

        # Son de l'appareil photo
        self.photo_sound = mixer.Sound("res/sound/photo.wav")

    def load_music(self, filename):
        mixer.music.load(filename)
        mixer.music.set_volume(0.1)
        mixer.music.play(-1)

    def load_music_queue(self, musics):
        [mixer.music.queue("res/music/%s.mp3" % music) for music in self.musics[1:]]

    def loop_sound(self, filename):
        sound = mixer.Sound(filename)
        sound.set_volume(0.4)
        sound.play(loops=-1)

    def load_sound(self, filename):
        sound = mixer.Sound(filename)
        sound.set_volume(0.4)
        return sound

    @staticmethod
    def play():
        mixer.music.play(-1)

    @staticmethod
    def stop():
        mixer.music.stop()

    def page_sound(self):
        self.page[randint(0, 8)].play()
