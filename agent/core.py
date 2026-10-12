"""Read-only issue investigation with safe, auditable agent stages."""
from pathlib import Path
import re

ALLOWED = {".py", ".md", ".txt", ".toml", ".yml", ".yaml"}
SKIP = {".git", "node_modules", ".venv", "__pycache__", "artifacts", "workspace"}


def collect_source(root: str, query: str, limit: int = 8) -> list[dict]:
    root_path = Path(root).resolve()
    if not root_path.is_dir():
        raise ValueError("Repository root not found")
    words = set(re.findall(r"[a-zA-Z_]{3,}", query.lower()))
    matches = []
    for path in root_path.rglob("*"):
        if any(part in SKIP for part in path.relative_to(root_path).parts):
            continue
        if not path.is_file() or path.suffix not in ALLOWED or path.stat().st_size > 100_000:
            continue
        content = path.read_text(encoding="utf-8", errors="replace")[:16000]
        score = sum(content.lower().count(word) for word in words)
        if score:
            matches.append({"path": str(path.relative_to(root_path)), "score": score, "excerpt": content[:2500]})
    matches.sort(key=lambda x: -x["score"])
    return matches[:limit]


def plan(issue_title: str, issue_body: str, root: str) -> dict:
    issue = (issue_title + "\n" + issue_body)[:5000]
    context = collect_source(root, issue)
    return {"stage": "proposal", "issue": issue, "files": context,
            "next_steps": ["Review relevant source", "Draft a minimal patch", "Request human approval", "Run isolated tests", "Open draft PR for review"]}
