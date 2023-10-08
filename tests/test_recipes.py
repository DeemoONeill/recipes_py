import json

import pytest

import recipes as rc


@pytest.fixture
def recipe_dict():
    with open("recipes.json") as file_handle:
        recipes = json.loads(file_handle.read())
    return {
        key: rc.Recipe(
            name=key,
            portions=value["portions"],
            ingredients={
                name: rc.Ingredient(name, *ingredient)
                for name, ingredient in value["ingredients"].items()
            },
        )
        for key, value in recipes.items()
    }


def test_shopping_list(recipe_dict):
    selection = [("carbonara", 2)]
    shopping_list = rc.make_shopping_list(selection, recipes=recipe_dict)

    assert shopping_list == {
        "egg": rc.Ingredient("egg", 2, "unit"),
        "parmesan cheese": rc.Ingredient("parmesan cheese", 200, "g"),
        "spaghetti": rc.Ingredient("spaghetti", 200, "g"),
        "bacon": rc.Ingredient("bacon", 4, "rashers"),
    }


def test_shopping_list2(recipe_dict):
    selection = [("carbonara", 4)]
    shopping_list = rc.make_shopping_list(selection, recipes=recipe_dict)

    assert shopping_list == {
        "egg": rc.Ingredient("egg", 4, "unit"),
        "parmesan cheese": rc.Ingredient("parmesan cheese", 400, "g"),
        "spaghetti": rc.Ingredient("spaghetti", 400, "g"),
        "bacon": rc.Ingredient("bacon", 8, "rashers"),
    }


def test_recipe(recipe_dict):
    """ "carbonara": {
        "ingredients": {
            "egg": 2,
            "parmesan cheese": 1,
            "spaghetti": 1,
            "bacon": 4
        },
        "portions": 2
    },"""
    carb: rc.Recipe = recipe_dict["carbonara"]
    portions = 2

    assert carb.ingredient_quantity(2) == carb.ingredients
    assert carb.ingredient_quantity(2.0) is carb.ingredients
    assert carb.ingredient_quantity(1.0) == {
        ingredient: quant / portions for ingredient, quant in carb.ingredients.items()
    }
    assert carb.ingredient_quantity(4) == {
        "egg": rc.Ingredient("egg", 4, "unit"),
        "parmesan cheese": rc.Ingredient("parmesan cheese", 400, "g"),
        "spaghetti": rc.Ingredient("spaghetti", 400, "g"),
        "bacon": rc.Ingredient("bacon", 8, "rashers"),
    }
