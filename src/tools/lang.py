"""
Ce module comprend une fonction qui a pour but de lire les fichiers .lang
Les fichiers de données .lang sont inspirés de ce dans le jeu Minecraft.
"""

# pylint: disable=consider-using-f-string

import os

def get_langs():
    """
    Retourne la liste de tous les noms des fichiers .lang
    """
    return [
        lang.replace(".lang", "") for lang in os.listdir("res/lang")
    ]

def load_lang(file):
    """
    Benchmark :
    100000 lignes : 0.197 secondes
    ~ 0,00000197/lignes
    """

    with open("res/lang/%s.lang" % file, 'r', encoding="utf-8") as file:
        lines = file.readlines()

    words = {}
    for line in lines:
        # Ignorer les commentaires
        if line.startswith('##') or not line:
            continue

        # Diviser la ligne en deux parties, séparées par le premier signe égal
        index = line.find('=')
        if index != -1:
            key = line[:index]
            valeur = line[index+1:].strip()
            words[key] = valeur

    return words

if __name__ == '__main__':
    words = load_lang('en.lang')

    print(words['accessibility.disableTTS']) # affiche 'Text To Speech disabled'
    print(words['accessibility.enableTTS']) # affiche 'Text To Speech enabled'
