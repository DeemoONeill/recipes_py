from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import template_me

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return template_me.template.render(recipes=template_me.recipes)


@app.get("/selected/{selected_recipe}")
async def read_item(selected_recipe: str):
    return {"selected_recipe": selected_recipe}
