# we want recipes, minimum: name, ingredients

recipes = {
    "carbonara": {
        "egg": 2,
        "parmesan cheese": 1,
        "spaghetti": 1,
        "bacon": 4,
    },
    "bacon and egg muffins": {
        "egg": 1,
        "english muffins": 1,
        "bacon": 2,
        "butter": 1,
    },
    "beef keema": {
        "rice": 1,
        "beef mince": 1,
        "curry powder": 1,
        "carrot": 2,
        "ginger": 1,
        "garlic clove": 3,
        "coriander": 1,
        "chicken stock": 1,
    },
    "carrot soup": {
        "carrot": 5,
        "onion": 2,
        "coriander": 1,
        "garlic clove": 1,
        "pepper": 1,
        "vegetable stock": 2,
    },
}

# dict(rice=1, carrot=2, beef_mince=3, garlic_clove=1)
shopping_list = {}


# we want to be able to select multiple recipes
list_of_wanted_recipes = []
# input
while True:
    print("available recipes: {}".format(recipes.keys()))
    selection = (
        input("What recipes do you want to select? (type done to finish): ")
        .lower()
        .strip()
        .strip(".")
    )

    if selection == "done":
        break

    try:
        portions = int(
            input("how many portions do you want to cook?: ").strip().strip(".")
        )
    except ValueError:
        print("not a valid portion, please make it a number")
        continue

    if selection not in recipes:
        print("not in recipe list")
        continue

    list_of_wanted_recipes.extend([selection] * portions)


# we want to aggregate all the ingredients from those, to make a shopping list
ingredient: list

for key in list_of_wanted_recipes:
    # loop through the ingredients in each recipe
    for ingredient, quantity in recipes[key].items():
        # loop through each ingredient in each list
        if ingredient in shopping_list:
            # if the ingredient has shown up before, add 1 to it
            shopping_list[ingredient] += quantity
        else:
            # if the ingredient has never shown up before, its the first time
            # so we set it to 1
            shopping_list[ingredient] = quantity

print(shopping_list)
