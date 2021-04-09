import re
from dateutil import parser
from typing import List, Tuple
import httpx

from .models import Repo


github_mdlink_pattern = re.compile(r"\[\w*\]\(https:\/\/github\.com\/(\w*\/\w*)\)")

def parse_links(md_text: str) -> List[Tuple[str, str]]:
    return re.findall(github_mdlink_pattern, md_text)


async def fetch_repo(client: httpx.Client, repo_full_name: str) -> Repo:
    r = await client.get(f"https://api.github.com/repos/{repo_full_name}")
    if r.status_code != httpx.codes.OK:
        return
    data = r.json()
    return Repo(
        full_name=repo_full_name,
        stars=data["stargazers_count"],
        last_push=parser.isoparse(data["pushed_at"])
    )

async def fetch_awesome_list(client: httpx.Client, repo_full_name: str) -> str:
    breakpoint()
    r = await client.get(f"https://api.github.com/repos/{repo_full_name}")
    branch = r.json()["default_branch"]
    r = await client.get(f"https://raw.githubusercontent.com/{repo_full_name}/{branch}/README.md")
    return r


async def main():
    async with httpx.AsyncClient() as client:
        r = await fetch_awesome_list(client, "vinta/awesome-python")
        print([await fetch_repo(client, full_name) for full_name in parse_links(r.text)])
