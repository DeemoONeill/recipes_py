# TODO create a script that turns a csv file into the same format as the recipes.json file, this should be used to bulk upload new recipes using the inputter.csv file

import csv
import json
import re

recipe_name = ""
rows = []

# read the file into this
with open("dhal_with_roasted_cauliflower.csv", encoding="utf - 8") as FH:
    reader = csv.reader(FH)
    # print(header)
    recipe_name = next(FH)
    rows = [row for row in reader]


# structure the data here
split_recipe_name = recipe_name.strip().split(",")
cleaned_recipe_name = split_recipe_name[0]


ingredients = {}
for value, key in rows:
    # need to split the value of the ones with both weight and measure
    unit = ""
    measure = ""
    for char in value:
        if char.isalpha():
            unit += char
        elif not char.isalpha():
            measure += char
    ingredients[key] = [measure, unit]


# export this out to json
with open("output.json", "w") as output:
    recipe = {cleaned_recipe_name: {"ingredients": ingredients, "portions": 2}}
    print(recipe)
    json.dump(recipe, output)
