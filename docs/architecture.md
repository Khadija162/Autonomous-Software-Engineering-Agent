# 10–16 week roadmap and security boundaries

**Implemented:** read-only repository exploration, issue proposal workflow, tree-sitter Python parsing, Ollama-compatible open-weight coding model adapter (opt-in), FastAPI backend, Streamlit frontend, unit tests, Docker Compose and CI. Local host-only Docker test utility has fixed commands and restrictive options; it is NOT exposed through the API.

**Not yet implemented:** autonomous file modification or debugging loops, production safe isolation for arbitrary GitHub repositories, automatic GitHub draft PR creation, SWE-bench evaluation, Azure managed deployments, approvals and tenant authorization.

**Weeks 1–4:** code indexing, chunking, tree-sitter symbol extraction and issue state persistence. **Weeks 5–8:** constrained patch generation, diff review and isolated test runner. **Weeks 9–12:** bounded reflection loops, draft PR creation after approval, regression checks and SWE-bench harness. **Weeks 13–16:** Azure Container Apps/AKS isolated execution, identity/Key Vault, monitoring, audit log, security and load evaluation.

Never mount a Docker socket or write-enabled GitHub tokens into untrusted model/execution containers. Public-facing deployments need authentication, per-repo ACLs, quotas and SSRF protection.
