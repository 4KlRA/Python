fruit_calories = {"APPLE": 130,
        "AVOCADO": 50,
        "BANANA": 110,
        "CANTALOUPE": 50,
        "GRAPEFRUIT": 60,
        "GRAPES": 90,
        "HONEYDEW MELON": 50,
        "KIWIFRUIT": 90,
        "LEMON": 15,
        "LIME": 20,
        "NECTARINE": 60,
        "ORANGE": 80,
        "PEACH": 60,
        "PEAR": 100,
        "PINEAPPLE": 50,
        "PLUMS": 70,
        "STRAWBERRIES": 50,
        "SWEET CHERRIES": 100,
        "TANGERINE": 50,
        "WATERMELON": 80,
}

fruit = input("Item: ").strip()

if(fruit.upper() in fruit_calories):
    print("Calories: ", fruit_calories[fruit.upper()])