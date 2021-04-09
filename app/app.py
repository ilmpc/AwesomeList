from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import datetime as dt

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

data = [{"name": "repo_name", "stars": 100, "push_date": dt.datetime(2020, 11, 29)}]


@app.get("/alive")
async def hi():
    return "I'm alive!"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, star_ascending: bool = True):
    now = dt.datetime.now()
    prepared_data = [
        {**repo, "days_from_push": (now - repo["push_date"]).days} for repo in data
    ]
    return templates.TemplateResponse(
        "index.html", {"request": request, "repos": prepared_data}
    )
