# update_projects.py
# Fetches your public GitHub repos via the GitHub API.
# Generates a projects.json file with repo details.
# This file is used by your Session 2 portfolio (script.js) to show projects.
# Runs automatically on every push via GitHub Actions.

import requests
import json
import os
from datetime import datetime

GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "your-username")

# These repos will be pinned/shown first if they exist
FEATURED_REPOS = ["folio", "pulse"]

def fetch_repos():
    """Fetch all public repos from GitHub API."""
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
    """Turn a GitHub repo dict into a clean project card dict."""
    # Pick a language tag - fall back to "Code" if GitHub doesn't know
    language = repo.get("language") or "Code"

    # Use description if it exists, otherwise a default
    description = repo.get("description") or "No description provided."

    return {
        "name": repo["name"],
        "description": description,
        "language": language,
        "stars": repo.get("stargazers_count", 0),
        "forks": repo.get("forks_count", 0),
        "url": repo.get("html_url", "#"),
        "homepage": repo.get("homepage") or "",
        "topics": repo.get("topics", []),
        "updated": repo.get("updated_at", "")[:10],  # just the date part
        "featured": repo["name"].lower() in FEATURED_REPOS
    }

def generate_projects_json(repos):
    """Build the full projects.json structure."""
    if not repos:
    repos = []

    # Build cards for all repos, excluding forks if you want
    cards = []
    for repo in repos:
        # Skip forked repos - only show your own work
        cards.append(build_project_card(repo))

    # Sort: featured repos first, then by updated date
    cards.sort(key=lambda x: (not x["featured"], x["updated"]), reverse=False)
    cards.sort(key=lambda x: not x["featured"])

    output = {
        "generated_at": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "username": GITHUB_USERNAME,
        "total": len(cards),
        "projects": cards
    }

    with open("projects.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"projects.json generated with {len(cards)} projects.")

    # Print a quick preview
    for card in cards[:3]:
        print(f"  - {card['name']} ({card['language']}): {card['description'][:50]}")

def run():
    """Fetch repos and write projects.json."""
    print(f"Fetching repos for GitHub user: {GITHUB_USERNAME}")
    repos = fetch_repos()

    if not repos:
        print("No repos fetched. Check your GITHUB_USERNAME secret.")
        return

    print(f"Found {len(repos)} repos.")
    generate_projects_json(repos)

if __name__ == "__main__":
    run()
