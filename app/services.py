import re


def parse_links(input):
    pattern = re.compile(r"\[(\w*)\]\(https:\/\/github\.com\/(\w*\/\w*)\)")
    return re.findall(pattern, input.read())


with open("foo.md", "r") as input:
    links = parse_links(input)


async def get_data(client, repo_full_name):
    r = await client.get(f"https://api.github.com/api/{repo_full_name}")
    data = r.json()
    last_push_date = data["pushed_at"]
    stars = data["stargazers_count"]
    return (last_push_date, stars)
