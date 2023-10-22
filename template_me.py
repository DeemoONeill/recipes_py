from jinja2 import Template
import json

with open("index.html.jinja") as fh:
    template = Template(fh.read())

with open("recipes.json") as fh:
    recipes = json.load(fh)

with open("index.html", "w") as fh:
    fh.write(template.render(recipes=recipes))
