import csv
import json
import re
from pathlib import Path

import click

measures_re = re.compile(r"(?P<measure>[\d\.]+)?\s?(?P<unit>[\w\s]+)?")


def recipe_builder(filename):
    # read the file into this
    recipe_name = ""
    rows = []
    filename = Path(filename)
    if filename.suffix != ".csv":
        return {}

    with open(filename, encoding="utf - 8") as FH:
        reader = csv.reader(FH)
        # print(header)
        recipe_name = next(FH)
        rows = [row for row in reader]

    # structure the data here
    split_recipe_name = recipe_name.strip().split(",")
    cleaned_recipe_name, portion = split_recipe_name
    if portion:
        portion = int(portion)
    else:
        portion = 4

    ingredients = {}
    for value, key in rows:
        # need to split the value of the ones with both weight and measure
        matched = re.match(measures_re, value)
        if not matched:
            continue
        measure, unit = matched.groups()
        measure = float(measure) if measure else 0
        unit = unit.strip() if unit else "unit"
        if unit == "to serve":
            continue
        if not key.strip():
            continue
        if key in ingredients:
            if measure == 0 and unit == "unit":
                continue
        ingredients[key] = [float(measure) if measure else float(), unit]

    return {cleaned_recipe_name: {"ingredients": ingredients, "portions": portion}}


@click.command()
@click.argument("filename")
@click.option("-o", "--output", default=None, type=Path)
def click_main(filename, output):
    filename = Path(filename)
    if filename.is_file():
        recipe = recipe_builder(filename)

    if filename.is_dir():
        recipe = {}
        for file in filename.iterdir():
            recipe.update(recipe_builder(file))
    # export this out to json
    if output is None:
        output = filename.with_suffix(".json")

    if output.exists():
        with open(output, "r", encoding="utf-8") as fh:
            existing: dict = json.load(fh)
        existing.update(recipe)
        recipe = existing

    with open(output, "w") as output:
        # print(recipe)
        json.dump(recipe, output, indent=4)


if __name__ == "__main__":
    click_main()
