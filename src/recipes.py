"""module for generating shopping lists from ingredients"""
# we want recipes, minimum: name, ingredients
import json

import pyinputplus as pyin

Units = str
"""Units for ingredients"""
Volume = int | float
"""Quantity of ingredients"""


class Ingredient:
    def __init__(
        self,
        name: str,
        volume: Volume,
        unit_of_measure: Units,
        measures_dict: dict[Units, Volume] | None = None,
    ):
        if measures_dict is None:
            measures_dict = {}
        self.measures_dict = measures_dict
        self.name = name
        self.volume = volume
        self.unit_of_measure = unit_of_measure

        if unit_of_measure in self.measures_dict:
            self.measures_dict[unit_of_measure] += volume
        else:
            self.measures_dict[unit_of_measure] = volume

    def __str__(self):
        return f"{self.name}: {self.measures_dict}"

    def __repr__(self):
        return str(self)

    def __add__(self: "Ingredient", other: "Ingredient"):
        if not isinstance(other, Ingredient):
            raise NotImplementedError(f"{other} is not an Ingredient")

        if self.name != other.name:
            raise ValueError("not the same type of ingredient")

        return self.__class__(
            self.name, other.volume, other.unit_of_measure, self.measures_dict.copy()
        )

    def __truediv__(self, other: int | float):
        if not isinstance(other, (int, float)):
            raise NotImplementedError(f"{other} is not a number")

        new_dict = {
            unit: quantity / other for unit, quantity in self.measures_dict.items()
        }
        return self.__class__(
            self.name,
            0,
            self.unit_of_measure,
            new_dict,
        )

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            raise NotImplementedError(f"{other} is not an Ingredient")

        if self.name != other.name:
            return False

        return self.measures_dict == other.measures_dict


### TODO: try to get recipe selection to be a dict of recipe to portion size.
###  i.e. carbonara 1 portion would be half of all the ingredients.
class Recipe:
    """The representation of a recipe"""

    def __init__(self, name, ingredients: dict[str, list[int, str]], portions):
        self.name = name

        # we want to normalise this to get the ingredients for a single portion
        self._normalised_ingredients = {
            ingredient: [quantity / portions, unit]
            for ingredient, (quantity, unit) in ingredients.items()
        }

        self.ingredients = ingredients

        self.portions = portions

    def ingredient_quantity(self, portions_to_cook: int | float):
        """This will give you back the amount of ingredients based on the number of portions you wish to cook"""
        if portions_to_cook == self.portions:
            return self.ingredients

        return {
            ingredient: [quantity * portions_to_cook, unit]
            for ingredient, (quantity, unit) in self._normalised_ingredients.items()
        }

    def __str__(self):
        return f"A recipe for {self.name}, that serves {self.portions}"

    def __repr__(self) -> str:
        return (
            f"Recipe(name='{self.name}', "
            + f"ingredients={self.ingredients}, "
            + f"portions={self.portions})"
        )


# we want to be able to select multiple recipes
def recipe_selection(recipes: dict[str, Recipe]):
    list_of_wanted_recipes = []
    # input
    valid_choices = list(recipes.keys())
    while True:
        selection: str = pyin.inputChoice(
            valid_choices, strip=True, caseSensitive=False, blank=True
        )

        if not selection:
            break

        recipe = recipes[selection]
        # recipes = {"carbonara", Recipe("carbonara", ingredients, portions)}
        # var = recipes["carbonara"] -> Recipe("carbonara")
        # var = Recipe("carbonara")
        # var.name == "carbonara"
        # var.portions == 2

        print(f"This recipe makes {recipe.portions} portions.")

        portions: int = pyin.inputNum(
            "If you want a different number please enter it here: ",
            default=recipe.portions,
            strip=True,
            min=1,
            blank=True,
        )

        if not portions:
            portions = recipe.portions

        list_of_wanted_recipes.append((selection, portions))

    return list_of_wanted_recipes


# we want to aggregate all the ingredients from those, to make a shopping list


def make_shopping_list(
    selections: list[tuple[str, int]], recipes: dict[str, Recipe]
) -> dict:
    """This function takes a list of recipe selections and
    returns a shopping list
    """

    shopping_list = {}
    for key, portions in selections:
        # loop through the ingredients in each recipe
        # get our selection from the recipes dict
        selection = recipes[key]
        # calculated the ingredients for the requested portions
        ingredients = selection.ingredient_quantity(portions)
        for ingredient, quantity in ingredients.items():
            # loop through each ingredient in each list
            if ingredient in shopping_list:
                # if the ingredient has shown up before, add 1 to it
                shopping_list[ingredient] += quantity
            else:
                # if the ingredient has never shown up before, its the first time
                # so we set it to 1
                shopping_list[ingredient] = quantity
    # TODO do a .join(selection list) to join the number and the measure together
    return shopping_list


def main():
    with open("recipes.json") as file_handle:
        recipes: dict[str, dict] = json.loads(file_handle.read())

    recipes = {key: Recipe(name=key, **value) for key, value in recipes.items()}

    selections = recipe_selection(recipes)
    shopping_list = make_shopping_list(selections, recipes)
    print(shopping_list)


if __name__ == "__main__":
    main()
