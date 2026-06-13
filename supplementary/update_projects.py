import requests
import json
import os
from datetime import datetime

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "AnandhanThampi")
FEATURED_REPOS = ["folio", "pulse"]

def fetch_repos():
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=30"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Could not fetch repos: {e}")
        return []

def build_project_card(repo):
    language = repo.get("language") or "Code"
    description = repo.get("description") or "No description provided."
    return {
        "name": repo["name"],
        "description": description,
        "language": language,
        "stars": repo.get("stargazers_count", 0),
        "url": repo.get("html_url", "#"),
        "updated": repo.get("updated_at", "")[:10],
        "featured": repo["name"].lower() in FEATURED_REPOS
    }

def run():
    print(f"Fetching repos for: {GITHUB_USERNAME}")
    repos = fetch_repos()
    print(f"Found {len(repos)} repos.")

    cards = [build_project_card(r) for r in repos]
    cards.sort(key=lambda x: not x["featured"])

    output = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "username": GITHUB_USERNAME,
        "total": len(cards),
        "projects": cards
    }

    with open("projects.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"projects.json written with {len(cards)} projects.")

if __name__ == "__main__":
    run()