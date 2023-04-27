"""
Le code  définit une fonction "memoize"  qui  stocke les résultats  de calculs
coûteux afin d'éviter de les recalculer à chaque fois qu'ils sont nécessaires.
La  fonction prend une autre fonction  comme argument  et renvoie une nouvelle
fonction qui utilise un dictionnaire  pour stocker les résultats.   Lorsque la
nouvelle  fonction  est appelée  avec  des arguments, elle essaie  de renvoyer
directement  le résultat stocké. S'il  n'existe   pas  alors  elle  appelle la
fonction avec ces arguments, stocke le résultat dans le cache et le renvoie.
"""

def memoize(func):
    """
    Décorateur qui créé un cache pour la fonction décoré, cette version est
    très  optimisée  car  elle  utilise un  try  et  non  une  vérification
    d'appartenance dans le cache. 
    """
    cache = {}

    def wrapper(*args):
        try:
            return cache[args]
        except KeyError:
            result = func(*args)
            cache[args] = result
            return result

    return wrapper
