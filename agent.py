"""AI SRE agent. One file, built up in steps, picked with AGENT_STEP:

  1  a bare model behind an HTTP endpoint
  2  + an identity: system prompt assembled from prompts/*.md
  3  + eyes: Bronto's MCP tools, so it can search real logs and traces
"""

import os

from strands import Agent

from app import MODEL_ID, REGION, answer, app, model

STEP = int(os.environ.get("AGENT_STEP", "3"))


def build_agent() -> Agent:
    kwargs = {"model": model, "callback_handler": None}
    if STEP >= 2:
        from identity import SYSTEM_PROMPT
        kwargs["system_prompt"] = SYSTEM_PROMPT
    if STEP >= 3:
        from tools import bronto_mcp
        kwargs["tools"] = [bronto_mcp()]
    return Agent(**kwargs)


@app.entrypoint
def invoke(payload: dict) -> dict:
    try:
        agent = build_agent()
        result = agent(payload.get("prompt", "Hello!"))
    except Exception as e:  # expired keys, no model access, Bronto unreachable...
        return {"error": f"{type(e).__name__}: {e}"}
    return {"result": answer(result, payload.get("reasoning", False))}


if __name__ == "__main__":
    print(f"AI SRE agent, step {STEP}, {MODEL_ID} in {REGION}", flush=True)
    print("""Try: curl -s localhost:8080/invocations -d '{"prompt": "Who are you?"}'""", flush=True)
    app.run()
