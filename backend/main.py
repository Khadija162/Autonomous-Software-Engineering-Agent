"""Local-only API; does not run untrusted code or push changes to GitHub."""
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from agent.core import plan
from agent.llm import propose

app = FastAPI(title="Autonomous Software Engineering Agent (review-first)", version="0.1.0")


class Request(BaseModel):
    title: str = Field(min_length=3, max_length=240)
    description: str = Field(max_length=5000)


@app.get("/health")
def health():
    return {"status": "ok", "mode": os.getenv("LLM_MODE", "mock")}


@app.post("/api/issues/analyze")
def analyze(issue: Request):
    root = os.getenv("AGENT_REPO_ROOT", "./sample_repo")
    try:
        report = plan(issue.title, issue.description, root)
        return {"investigation": report, "model": propose(report),
                "side_effects": "none", "approval_required": True}
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
