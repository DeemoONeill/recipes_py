"""module for generating shopping lists from ingredients"""
# we want recipes, minimum: name, ingredients
import json

import pyinputplus as pyin  # type: ignore

Units = str
"""Units for ingredients"""
Volume = int | float
"""Quantity of ingredients"""


class Ingredient:
    """Takes an ingredient and creates an instance of that ingredient with weights and
    units of measure"""

    def __init__(
        self,
        name: str,
        volume: Volume | str | None = None,
        unit_of_measure: Units | None = None,
        measures_dict: dict[Units, Volume] | None = None,
    ):
        if measures_dict is None:
            measures_dict = {}
        self.measures_dict = measures_dict
        self.name = name
        if not isinstance(volume, (int, float)):
            volume = float(volume) if volume is not None else float()
        if unit_of_measure and volume:
            self.measures_dict[unit_of_measure.lower()] = volume

    def __str__(self):
        quantities = ", ".join(
            [f"{quantity} {unit}" for unit, quantity in self.measures_dict.items()]
        )
        return f"{self.name}: {quantities}"

    def __repr__(self):
        return f"Ingredient('{self.name}', None, None, {self.measures_dict})"

    def __add__(self: "Ingredient", other: "Ingredient"):
        if not isinstance(other, Ingredient):
            raise NotImplementedError(f"{other} is not an Ingredient")

        if self.name != other.name:
            raise ValueError("not the same type of ingredient")
        measures_1 = self.measures_dict
        measures_2 = other.measures_dict
        all_units = set(self.measures_dict.keys()).union(other.measures_dict.keys())

        new_dict = {
            unit: measures_1.get(unit, 0) + measures_2.get(unit, 0)
            for unit in all_units
        }

        return self.__class__(self.name, None, None, new_dict)

    def __truediv__(self, portions: int | float):
        if not isinstance(portions, (int, float)):
            raise NotImplementedError(f"{portions} is not a number")

        new_dict = {
            unit: quantity / portions for unit, quantity in self.measures_dict.items()
        }
        return self.__class__(self.name, None, None, new_dict)

    def __mul__(self, portions: int | float):
        if not isinstance(portions, (int, float)):
            raise NotImplementedError(f"{portions} is not a number")

        # measures dict is {unit: amount} e.g. {"g": 200, "unit": ,10}
        # unit amount, multiplying by the portions, which is other.

        new_dict = {
            unit: quantity * portions for unit, quantity in self.measures_dict.items()
        }
        return self.__class__(self.name, None, None, new_dict)

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            raise NotImplementedError(f"{other} is not an Ingredient")

        if self.name != other.name:
            return False

        return self.measures_dict == other.measures_dict


class Recipe:
    """The representation of a recipe"""

    def __init__(self, name, ingredients: dict[str, Ingredient], portions):
        self.name = name

        # we want to normalise this to get the ingredients for a single portion
        self._normalised_ingredients = {
            ing_name: ingredient / portions
            for ing_name, ingredient in ingredients.items()
        }

        self.ingredients = ingredients

        self.portions = portions

    def ingredient_quantity(self, portions_to_cook: int | float):
        """This will give you back the amount of ingredients based on the number of
        portions you wish to cook"""
        if portions_to_cook == self.portions:
            return self.ingredients

        return {
            ing_name: ingredient * portions_to_cook
            for ing_name, ingredient in self._normalised_ingredients.items()
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
    """Prompts the user for which recipes and quantities they want to cook"""
    list_of_wanted_recipes = []
    # input
    list_of_recipes = list(recipes.keys())
    valid_choices = list(enumerate(list_of_recipes, start=1))

    while True:
        print("please select one of the following recipes:")
        for i in range(0, len(valid_choices), 4):
            print(
                *[f"{num}: {recipe}" for num, recipe in valid_choices[i : i + 4]],
                sep=" -- ",
            )
        choices = [str(number) for number, _ in valid_choices]
        selection: str = pyin.inputChoice(choices, strip=True, blank=True)

        if not selection:
            print("You have selected", *list_of_wanted_recipes)
            if pyin.inputBool(
                "is this correct?",
                caseSensitive=False,
                default=True,
            ):
                break
            continue
        selection = list_of_recipes[int(selection) - 1]
        print("selected:", selection)

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

    shopping_list: dict[str, Ingredient] = {}
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
    return shopping_list


def main():
    """Entry point"""
    with open("recipes.json", encoding="utf-8") as file_handle:
        recipes: dict[str, dict] = json.loads(file_handle.read())

    recipes = {
        key: Recipe(
            name=key,
            portions=value["portions"],
            ingredients={
                name: Ingredient(name, *ingredient)
                for name, ingredient in value["ingredients"].items()
            },
        )
        for key, value in recipes.items()
    }

    selections = recipe_selection(recipes)
    shopping_list = make_shopping_list(selections, recipes)
    with open("shopping_list.txt", "w", encoding="utf-8") as fh:
        print(*shopping_list.values(), file=fh, sep="\n")


if __name__ == "__main__":
    main()
