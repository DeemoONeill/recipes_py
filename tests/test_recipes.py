import json

import pytest

import recipes


@pytest.fixture
def recipe_dict():
    with open("recipes.json") as file_handle:
        return json.loads(file_handle.read())


def test_shopping_list(recipe_dict):
    selection = ["carbonara"]
    shopping_list = recipes.make_shopping_list(selection, recipes=recipe_dict)

    assert shopping_list == {
        "egg": 2,
        "parmesan cheese": 1,
        "spaghetti": 1,
        "bacon": 4,
    }


def test_shopping_list2(recipe_dict):
    selection = ["carbonara"] * 2
    shopping_list = recipes.make_shopping_list(selection, recipes=recipe_dict)

    assert shopping_list == {
        "egg": 4,
        "parmesan cheese": 2,
        "spaghetti": 2,
        "bacon": 8,
    }
