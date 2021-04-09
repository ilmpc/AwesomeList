from pydantic import BaseModel
import datetime as dt

class Repo(BaseModel):
    full_name: str
    stars: int
    last_push: dt.datetime
