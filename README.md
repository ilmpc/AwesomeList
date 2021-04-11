# App for investingating awesome repos

Deployed on [heroku](https://ilmpc-awesome-list.herokuapp.com/)

## Build using:
- Poetry
- FastAPI
- Jinja2
- HTTPX

## To run locally
1. `poetry install`
1. `create .env file with vars as described in app/config.py`
1. `python -m app`

## How it works

- Parse all links to github repos from README.md in awesome-x repo.
- Get info (stars, last commit date) about repos using Github API every 12h and store it in json file.
- Generate html page with all that info in table.