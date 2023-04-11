# La fonction  prend en entrée un  chemin  d'accès à un répertoire contenant des
# images. Elle parcourt récursivement le répertoire en utilisant  "os.walk" pour
# récupérer  la liste de tous les fichiers  d'images,  et charge  chaque image à
# l'aide de "pygame.image.load".
# 
# Les images sont stockées dans une liste et  renvoyées à la fin de la fonction.
# La  méthode "convert_alpha" est  utilisée pour  optimiser les  performances de
# l'affichage des images dans Pygame  en préparant les images  à une utilisation
# avec la transparence alpha.


from src.tools.memoize import memoize
import pygame
import os

@memoize
def get_images(path):
    surface_list = []
    for _, __, img_files in os.walk(path):
        for image in img_files:
            surface_list.append(
                pygame.image.load(os.path.join(path, image)).convert_alpha()
            )
    return surface_list
