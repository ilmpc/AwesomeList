from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import datetime as dt
import copy
import httpx

from .services import get_data

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

data = [{"name": "ilmpc/Algorithms", "stars": 100, "push_date": dt.datetime(2020, 11, 29)}]


@app.get("/alive")
async def hi():
    return "I'm alive!"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, star_ascending: bool = True):
    now = dt.datetime.now()
    prepared_data = []
    for repo in await get_data():
        copied_repo = copy.copy(repo)
        copied_repo.days_last_push = (now - repo.last_push).days
        prepared_data.append(copied_repo)
    return templates.TemplateResponse(
        "index.j2", {"request": request, "repos": prepared_data}
    )
