import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, PackageLoader, select_autoescape
from uvicorn import run

from recipes import Ingredient, Recipe, make_shopping_list

env = Environment(loader=PackageLoader("src"), autoescape=select_autoescape())

with open("recipes.json") as fh:
    recipes = json.load(fh)

recipe_classes = {
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

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return env.get_template("index.html.jinja").render(recipes=recipes)


@app.get("/selected", response_class=HTMLResponse)
async def read_item(request: Request):
    selected = request.query_params.getlist("recipe")
    selections = [recipe_classes.get(recipe) for recipe in selected]
    selections = [(recipe.name, recipe.portions) for recipe in selections]

    shopping_list = make_shopping_list(selections, recipe_classes)
    shopping_list = dict(sorted(shopping_list.items(), key=lambda x: x[0]))
    return env.get_template("selected.html.jinja").render(
        selections=selected,
        shopping_list=shopping_list,
    )


if __name__ == "__main__":
    run(app)
