# bedrock-agent-observability

An AI SRE agent on Amazon Bedrock, built step by step. It answers over HTTP,
takes its identity from plain Markdown files, and investigates incidents by
querying real logs and traces through Bronto's MCP server.

Based on the hands-on labs from the **AWS + Bronto "AI & Observability" evening**
(Dublin, September 2026): [AI SRE lab](https://aisre-lab.vercel.app/1) and
[Track A: Observability for AI](https://github.com/bronto-community/track-a-observability-for-ai).
I rebuilt the code here myself to learn it; notes on each step are in [`docs/log.md`](docs/log.md).

## Progress

- [x] **Step 1 — Model behind an endpoint.** Strands `Agent` on Bedrock, served by `BedrockAgentCoreApp` (`POST /invocations`, `GET /ping`).
- [x] **Step 2 — Identity.** System prompt assembled from `prompts/*.md` (role, rules, report format, personal style).
- [x] **Step 3 — Eyes.** Bronto MCP server wired in as tools: the agent can search logs and datasets.
- [ ] **Step 4** — _next_
- [ ] **Step 5** — _next_
- [ ] Observability of the agent itself: OpenTelemetry traces, tokens, latency and cost → Bronto dashboard
- [ ] Run on my own AWS account with a least-privilege IAM policy

## How it works

```
curl ──► agent.py ──► Strands Agent ──► Bedrock (Claude Haiku / Nova)
                         │
                         ├── system prompt ◄── prompts/*.md      (step 2)
                         └── tools ◄── Bronto MCP server        (step 3)
```

| File | What |
|---|---|
| `agent.py` | Entry point. `AGENT_STEP` (1–3) decides what the agent gets. |
| `app.py` | Model, HTTP app, and cleanup of reasoning text some models leak into answers |
| `identity.py` | Joins every `prompts/*.md` (alphabetical) into the system prompt |
| `tools.py` | Bronto MCP client |
| `prompts/` | The agent's identity, one concern per file |

## Run it

You need Docker, AWS credentials that can call Bedrock, and (for step 3) a Bronto API key.

```bash
cp .env.example .env        # then fill it in: no quotes around values
docker build -t ai-sre-agent .
docker run --rm -p 8080:8080 --env-file .env ai-sre-agent
```

In a second terminal:

```bash
curl -s localhost:8080/invocations -d '{"prompt": "Who are you?"}'
curl -s localhost:8080/invocations -d '{"prompt": "Any errors in the last hour?"}'
```

Change the agent's personality without rebuilding by mounting your own prompt file:

```bash
docker run --rm -p 8080:8080 --env-file .env \
  -v "$PWD/prompts/my.md:/app/prompts/my.md" ai-sre-agent
```

Run an earlier step: add `-e AGENT_STEP=1` (or `2`).

## Stack

Python · [Strands Agents](https://strandsagents.com) · Amazon Bedrock · Bedrock AgentCore runtime · MCP · Bronto · Docker
