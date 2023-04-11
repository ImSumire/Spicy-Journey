import os

def get_langs():
    return [
        lang.replace(".lang", "") for lang in os.listdir("res/lang")
    ]

def load_lang(file):
    """
    Benchmark :
    100000 lignes : 0.197 secondes
    ~ 0,00000197/lignes
    """

    with open("res/lang/%s.lang" % file, 'r') as f:
        lines = f.readlines()

    items = {}
    for line in lines:
        # Ignorer les commentaires
        if line.startswith('##') or not line:
            continue

        # Diviser la ligne en deux parties, séparées par le premier signe égal
        index = line.find('=')
        if index != -1:
            key = line[:index]
            valeur = line[index+1:].strip()
            items[key] = valeur

    return items

if __name__ == '__main__':
    items = load_lang('en.lang')

    print(items['accessibility.disableTTS']) # affiche 'Text To Speech disabled'
    print(items['accessibility.enableTTS']) # affiche 'Text To Speech enabled'

