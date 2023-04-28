"""
Liste des ingrédients dans un dictionnaire avec la liste des ingrédients.
Le '#' correspond au tag, affichage de 'Un'/'Any' dans le livre de recettes.
"""

# pylint: disable=consider-using-f-string

recipes = {
    "Hot Apple": ["apple"],
    "Wheat Bread": ["wheat"],
    "Mushroom Rice Balls": ["rice", "rice", "rice", "rice", "rice", "mushroom", "mushroom"],
    "Veggie Rice Balls": ["rice", "rice", "rice", "rice", "rice", "radish", "radish"],
    "Carrot Rice Balls": ["rice", "rice", "rice", "rice", "rice", "carrot", "carrot"],
    "Fried Wild Greens": ["radish", "radish", "radish", "carrot", "carrot", "carrot"],
    "Steamed Mushrooms With Radish": ["radish", "mushroom", "mushroom", "mushroom"],
    "Steamed Mushrooms With Carrot": ["carrot", "mushroom", "mushroom", "mushroom"],
    "Steamed Fruit": ["apple", "apple", "apple", "apple", "carrot", "carrot"],
    "Fruit and Mushroom Mix": ["apple", "apple", "apple", "mushroom", "mushroom", "mushroom"],
    "Mushroom Skewer": ["mushroom", "mushroom", "mushroom", "mushroom", "mushroom"],
    "Vegetable Risotto": ["rice", "rice", "rice", "carrot", "carrot"],
    "Mushroom Risotto": ["rice", "rice", "rice", "mushroom", "mushroom"],
    "Carrot Cake": ["wheat", "wheat", "wheat", "carrot", "carrot"],
}

if __name__ == "__main__":

    ingredients = []
    for v in recipes.values():
        for i in v:
            if i not in ingredients:
                ingredients.append(i)

    print("List of ingredients : %s" % (', '.join(sorted(ingredients))))
