recipes = {
    "Creamy Heart Soup": ["radish", "#fruit", "#fruit", "milk"],  # 6/5
    "Creamy Seafood Soup": ["milk", "salt", "#vegetable", "#fish"],  # 5/5
    "Carrot Cream Soup": ["milk", "salt", "carrot"],  # 4/5
    "Cream of Vegetable Soup": ["milk", "salt", "#vegetable"],  # 3/5
    "Meat and Seafood Fry": ["#meat", "#fish"],  # 2/5
    "Gourmet Meat and Seafood Fry": ["#meat", "#meat", "#fish", "#fish"],  # 1/5
    "Meat and Rice Bowl": ["rice", "salt", "#meat"],  # 1/4
    "Fried Egg and Rice": ["rice", "egg"],  # 5/3
    "Curry Pilaf": ["#spice", "rice", "butter"],  # 3/3
    "Vegetable Omelet": ["egg", "butter", "salt", "#vegetable"],  # 2/3
    "Prime Poultry Pilaf": ["rice", "egg", "butter", "chicken"],  # 1/3
    "Fragrant Mushroom Saute": ["#mushroom", "#spice"],  # 5/2
    "Salt-Grilled Prime Meat": ["#meat", "salt"],  # 4/2
    "Wheat Bread": ["wheat", "salt", "butter"],  # 2/2
    "Copious Fried Wild Greens": ["#vegetable"],  # 1/2
    "Salt-Grilled Mushrooms": ["#mushroom", "salt"],  # 5/1
    "Meat Skewer": ["#meat"],  # 1/1
    "Copious Meat Skewer": ["#meat", "#meat"],  # 2/1
    "Gourmet Skewer": ["#meat", "#meat", "#meat"],  # 3/1
    "Spiced Meat Skewer": ["#meat", "#spice"],  # 1/2
    "Prime Spiced Meat Skewer": ["#meat", "#meat", "#spice"],  # 2/2
    "Mushroom Skewer": ["#mushroom"],  # 6/2
    "Meat and Mushroom Skewer": ["#mushroom", "#meat"],  # 5/2
    "Steamed Mushrooms": ["#mushroom", "#herb"],  # 6/5
    "Baked Mushroom": ["#mushroom"],  # 2/6
    "Baked Apple": ["apple"],  # 4/6
    "Cooked Fish": ["#fish"],  # 5/6
    "Cooked Meat": ["#meat"],  # 6/6
}

if __name__ == "__main__":

    ingredients = []
    for v in recipes.values():
        for i in v:
            if i not in ingredients:
                ingredients.append(i)

    print("List of ingredients : %s" % (', '.join(sorted([_ for _ in ingredients]))))
