# TODO create a script that turns a csv file into the same format as the recipes.json file, this should be used to bulk upload new recipes using the inputter.csv file

import csv
import json

recipe_name = ""
rows = []

# read the file into this
with open("dhal_with_roasted_cauliflower.csv", encoding="utf - 8") as FH:
    reader = csv.reader(FH)
    # print(header)
    recipe_name = next(FH)
    rows = [row for row in reader]


# structure the data here
split_recipe_name = recipe_name.split(",")
cleaned_recipe_name = split_recipe_name[0]

ingredients = []
for row in rows:
    ingredients.extend(row)
ingredient_names = ingredients[1 : len(ingredients) : 2]


weights_and_measures = ingredients[0 : len(ingredients) : 2]
new_weights_and_measures = " ".join(weights_and_measures)
split_weights_and_measures = new_weights_and_measures.split(" ")
weights = split_weights_and_measures[0 : len(split_weights_and_measures) : 2]


recipe = {cleaned_recipe_name: {"ingredients": ingredient_names}}
print(recipe)

# export this out to json
