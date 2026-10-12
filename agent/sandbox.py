"""Explicitly approved host-side Docker test runner for trusted/local repository copies.
DO NOT expose this helper as an unauthenticated HTTP endpoint.
Docker isolation is defense-in-depth, not a strong guarantee against kernel exploits.
"""
from pathlib import Path
import subprocess


def run_pytest_in_docker(repo_dir: str, timeout: int = 120) -> dict:
    root = Path(repo_dir).resolve()
    if not root.is_dir() or not (root / "pyproject.toml").exists():
        raise ValueError("Expected approved repository directory with pyproject.toml")
    command = [
        "docker", "run", "--rm", "--network", "none", "--read-only",
        "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
        "--pids-limit", "64", "--memory", "512m", "--cpus", "1",
        "--user", "65534:65534", "--tmpfs", "/tmp:rw,nosuid,noexec,size=32m",
        "-v", f"{root}:/code:ro", "-w", "/code",
        "python:3.12-slim", "python", "-m", "unittest", "discover", "-v"
    ]
    # A fixed container image and fixed command avoid executing AI-authored shell text.
    try:
        completed = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        return {"exit_code": completed.returncode, "stdout": completed.stdout[-8000:],
                "stderr": completed.stderr[-3000:]}
    except subprocess.TimeoutExpired:
        return {"exit_code": 124, "stdout": "", "stderr": "Container test timeout"}
