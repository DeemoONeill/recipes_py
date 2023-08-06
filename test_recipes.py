import recipes


def test_shopping_list():
    selection = ["carbonara"]
    shopping_list = recipes.make_shopping_list(selection, recipes=recipes.recipes)

    assert shopping_list == {
        "egg": 2,
        "parmesan cheese": 1,
        "spaghetti": 1,
        "bacon": 4,
    }


def test_shopping_list2():
    selection = ["carbonara"] * 2
    shopping_list = recipes.make_shopping_list(selection, recipes=recipes.recipes)

    assert shopping_list == {
        "egg": 4,
        "parmesan cheese": 2,
        "spaghetti": 2,
        "bacon": 8,
    }
