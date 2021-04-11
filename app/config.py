from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    TOKEN: str = "" # Github API token
    CACHE_FILE: str = "repos.json" # File to store cache (downloaded info about repos)
    PORT: int = 8080 
    AWESOME_REPO: str = "vinta/awesome-python" # awesome repo that will be parsed

settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
