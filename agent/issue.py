"""Fetch a public GitHub issue via official GitHub API; no write privileges."""
import re
import os
import requests


def fetch_public_issue(owner: str, repo: str, number: int) -> dict:
    valid = r"[A-Za-z0-9_.-]{1,100}"
    if not re.fullmatch(valid, owner) or not re.fullmatch(valid, repo) or number < 1:
        raise ValueError("Invalid GitHub repository or issue")
    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    response = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/issues/{number}",
        headers=headers, timeout=15
    )
    response.raise_for_status()
    data = response.json()
    if "pull_request" in data:
        raise ValueError("Requested number is a pull request")
    return {"number": number, "title": data["title"], "body": data.get("body") or "",
            "url": data["html_url"]}
