# we want recipes, minimum: name, ingredients
import pyinputplus as pyin

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


# we want to be able to select multiple recipes
def recipe_selection(recipes):
    list_of_wanted_recipes = []
    # input
    valid_choices = ["done"]
    valid_choices.extend(recipes.keys())
    while True:
        selection = pyin.inputChoice(valid_choices, strip=True, caseSensitive=False)

        if selection == "done":
            break

        portions = pyin.inputNum(
            "how many portions do you want to cook?: ", default=1, strip=True, min=1
        )

        list_of_wanted_recipes.extend([selection] * portions)
    return list_of_wanted_recipes


# we want to aggregate all the ingredients from those, to make a shopping list


def make_shopping_list(selections: list, recipes: dict) -> dict:
    """This function takes a list of recipe selections and
    returns a shopping list
    """

    shopping_list = {}
    for key in selections:
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
    return shopping_list


def main():
    selections = recipe_selection(recipes)
    shopping_list = make_shopping_list(selections, recipes)
    print(shopping_list)


if __name__ == "__main__":
    main()
