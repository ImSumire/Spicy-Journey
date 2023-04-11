# Le code  définit une fonction "memoize"  qui  stocke les résultats  de calculs
# coûteux afin d'éviter de les recalculer à chaque fois qu'ils sont nécessaires.
# La  fonction prend une autre fonction  comme argument  et renvoie une nouvelle
# fonction qui utilise un dictionnaire  pour stocker les résultats.   Lorsque la
# nouvelle  fonction  est appelée  avec  des arguments, elle essaie  de renvoyer
# directement  le résultat stocké. S'il  n'existe   pas  alors  elle  appelle la
# fonction avec ces arguments, stocke le résultat dans le cache et le renvoie.


def memoize(func):
    cache = {}

    def wrapper(*args):
        try:
            return cache[args]
        except:
            result = func(*args)
            cache[args] = result
            return result

    return wrapper
