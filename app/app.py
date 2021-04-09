from pathlib import Path
import datetime as dt
import copy
import json

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every
import aiofiles
import httpx

from .services import get_data

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

data = []

@app.get("/alive")
async def hi():
    return "I'm alive!"


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, star_ascending: bool = True):
    now = dt.datetime.now(dt.timezone.utc)
    prepared_data = []
    for repo in data:
        copied_repo = copy.copy(repo)
        copied_repo.days_last_push = (now - repo.last_push).days
        prepared_data.append(copied_repo)
    return templates.TemplateResponse(
        "index.j2", {"request": request, "repos": prepared_data}
    )

@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 12) #12h
async def update_cache():
    global data
    now = dt.datetime.timestamp()
    if Path(settings.cache_file).is_file():
        async with aiofiles.open(settings.cache_file) as cache:
            cache_data = json.load(cache)
            if now - cache_data[timestamp] < 60 * 60 * 12:
                data = cache_data[data]
                return
    
    data = await get_data()
    async with aiofiles.open(settings.cache_file, mode="w") as cache:
        cache_data = {"timestamp": now, "data": data}
        json.dump(cache_data, cache)