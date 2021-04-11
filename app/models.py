from pydantic import BaseModel
from typing import List
import datetime as dt


class Repo(BaseModel):
    full_name: str
    stars: int
    last_push: dt.datetime


class Repos(BaseModel):
    update_time: dt.datetime
    data: List[Repo]
