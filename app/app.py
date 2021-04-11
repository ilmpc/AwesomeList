from pathlib import Path
import datetime as dt
import copy
import json
from typing import Optional

from fastapi import FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_utils.tasks import repeat_every
from pydantic import ValidationError
import aiofiles
import httpx

from .services import get_data
from .config import settings
from .models import Repos

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

data = []


@app.get("/alive")
async def hi():
    return "I'm alive!"


selectors = {
    "name": lambda el: el.full_name,
    "stars": lambda el: el.stars,
    "days": lambda el: el.last_push,
}


@app.get("/", response_class=HTMLResponse)
async def index(
    request: Request, sort_by: Optional[str] = "name", ascending: Optional[bool] = True
):
    if sort_by not in selectors:
        raise HTTPException(status_code=400, detail="No such key to sort by")
    now = dt.datetime.now(dt.timezone.utc)
    return templates.TemplateResponse(
        "index.j2",
        {
            "request": request,
            "repos": sorted(data, key=selectors[sort_by], reverse=(not ascending)),
            "now": now,
            "sort_by": sort_by,
            "ascending": ascending,
        },
    )


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 12)
async def update_cache():
    global data
    now = dt.datetime.now(dt.timezone.utc)
    if Path(settings.CACHE_FILE).is_file():
        async with aiofiles.open(settings.CACHE_FILE) as cache:
            try:
                cache_data = Repos.parse_raw(await cache.read())
                if now - cache_data.update_time < dt.timedelta(hours=12):
                    data = cache_data.data
                    return
            except ValidationError:
                pass

    data = await get_data()
    async with aiofiles.open(settings.CACHE_FILE, mode="w") as cache:
        cache_data = Repos(update_time=now, data=data)
        await cache.write(cache_data.json())


@app.on_event("startup")
async def on_startup():
    await update_cache()
