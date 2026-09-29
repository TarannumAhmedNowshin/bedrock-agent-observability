# Build log

What I did, what broke, what I learned. Newest at the bottom.

## 2026-09-29 — Workshop night: steps 1–3

**Did:** Ran the lab's prebuilt images (`step-1`, `step-2`), then wrote the steps myself.

**Broke, and why:**

- `InvalidRegionError: '"us-west-2"'` — I wrote `AWS_REGION="us-west-2"` in `.env`.
  `docker --env-file` does **not** strip quotes (a shell or python-dotenv would), so the
  quotes became part of the value. Fix: no quotes in `.env` files for Docker.
- `curl` returned nothing — the container had already crashed. The server has to be running
  in one terminal and `curl` sent from another.
- `IsADirectoryError: prompts/my.md` — I bind-mounted `$PWD/my.md` before the file existed.
  When a `-v` source path doesn't exist, Docker creates it as an empty **directory**.
  Fix: create the file first.
- `Cannot connect to the Docker daemon` — Docker Desktop wasn't running after a restart.
- Workshop AWS credentials were temporary (`ASIA...` key + session token) and expired overnight.

**Learned:**

- An "agent" here is just: model + system prompt + tools, in a loop. Strands runs the loop.
- `BedrockAgentCoreApp` gives the HTTP contract AgentCore expects (`/invocations`, `/ping` on 8080),
  so the same code runs locally in Docker and in AWS.
- Keeping the identity in Markdown files means non-engineers can change agent behaviour
  without touching code or rebuilding the image.
- MCP lets the agent use another product's tools (Bronto's log search) without me writing them.

## 2026-09-30 — Cleaned up into a repo

- Fixed `agents.py`: it imported `Path` from `zipfile` instead of `pathlib`. Renamed it to
  `identity.py` (a local module named `agents` can also clash with the `agents` package on PyPI).
- `step3.py` was missing its imports (`MCPClient`, `streamable_http_client`, `httpx2`, `Agent`).
  Note: `mcp` 2.x uses `httpx2`, not `httpx`.
- Merged the step files into one `agent.py` with `AGENT_STEP`, so every step stays runnable.
- Errors (expired keys, Bronto unreachable) now come back as `{"error": ...}` instead of a crash.
