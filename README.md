# Autonomous Software Engineering Agent — Review-First Prototype

A practical **10–16 week enterprise software engineering agent roadmap** implemented as an initial, locally runnable project: issue investigation, source exploration, tree-sitter Python parsing, **open-weight coding LLM via Ollama**, FastAPI backend, Streamlit frontend, Docker and CI.

> **Maturity:** This is a **read-only working prototype**, not an autonomous PR-writing system yet. The AI proposes approaches, but never writes code or executes arbitrary commands via the API. GitHub issue fetching, host-side sandbox testing and cloud components are explicit building blocks, not a connected automatic issue-to-PR workflow.

## Architecture

```text
Issue description -> FastAPI -> issue analysis -> code retrieval -> Ollama coding model (or mock)
                                              -> source references + proposal -> Streamlit review
Optional tools: GitHub public issue fetcher, tree-sitter syntax checker, Docker unittest runner
Future: approval -> patch creation -> sandbox testing -> draft PR -> CI
```

## Run locally (Windows PowerShell)

```powershell
git clone https://github.com/Khadija162/Autonomous-Software-Engineering-Agent.git
cd Autonomous-Software-Engineering-Agent
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Run FastAPI in terminal 1:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload
```

Run Streamlit in terminal 2:

```powershell
.\.venv\Scripts\python.exe -m streamlit run frontend/app.py
```

- Backend: http://127.0.0.1:8000/docs
- Frontend: http://127.0.0.1:8501

The sample issue can be investigated even without API keys.

## Open-weight LLM

Default `LLM_MODE=mock` keeps all logic local and deterministic. To use actual model inference, install [Ollama](https://ollama.com/) and pull a compatible open-weight coding model, for example:

```powershell
ollama pull qwen2.5-coder:7b
$env:LLM_MODE="ollama"
$env:OLLAMA_MODEL="qwen2.5-coder:7b"
```

Restart the **locally running backend** in the same terminal session after setting these values. Ollama downloads model weights separately and requires sufficient RAM.

## Docker application

```powershell
docker compose up --build
```

The containerized demo defaults to mock inference, binds its web ports to localhost and does not mount a Docker socket.

## Safety

Issue text and repository contents are untrusted. The web API does not write repository files, execute proposed shell commands, run tests or push GitHub branches. A separate **host-side** `agent/sandbox.py` helper runs a fixed unittest discovery command in a restricted network-disabled container **only when explicitly invoked on a trusted local repository**. This is not a full security sandbox for adversarial code; disposable VMs or isolated managed runners are required for untrusted tasks.

## Included project components

| Location | What exists |
|---|---|
| `agent/core.py` | Repository exploration and evidence-based issue plan |
| `agent/issue.py` | Read-only public GitHub issue adapter |
| `agent/syntax.py` | tree-sitter Python parser |
| `agent/llm.py` | Mock or Ollama coding assistant |
| `agent/sandbox.py` | Explicit restricted Docker test helper |
| `backend/main.py` | FastAPI API |
| `frontend/app.py` | Streamlit frontend |
| `sample_repo/` | Original openly reusable fixture code/tests |
| `.github/workflows/` | CI tests and Docker build |
| `infra/terraform/` | Example Azure resource group and storage only |

## Azure and enterprise roadmap

**Target architecture (not deployed):** Azure Container Apps (web/backend), Azure Service Bus (agent jobs), Azure Blob Storage (logs/artifacts), isolated Azure Container Apps Jobs or AKS runners (untrusted tests), Key Vault and managed identity, Azure Monitor, and Ollama/vLLM-hosted open-weight models on appropriate dedicated compute. Adopt Azure AI Search or vector storage for codebase retrieval at scale.

See [architecture and 10–16 week plan](docs/architecture.md) and [open evaluation data](docs/data.md). Integrate SWE-bench evaluations only using isolated disposable compute and respecting source licenses.

**Status:** GitHub source has been uploaded; live Docker runs, CI results, model inference and Azure provisioning have not yet been verified. Azure resources are **not provisioned**.
