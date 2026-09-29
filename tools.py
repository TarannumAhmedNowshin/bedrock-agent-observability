"""The eyes: Bronto's MCP server. Its tools (search logs, list datasets, ...)
become tools the agent can call. Nothing connects until the agent uses it.
"""

import os

import httpx2
from mcp.client.streamable_http import streamable_http_client
from strands.tools.mcp import MCPClient


def bronto_mcp() -> MCPClient:
    api_key = os.environ.get("BRONTO_API_KEY")
    if not api_key:
        raise RuntimeError("BRONTO_API_KEY is not set: add it to .env (see .env.example)")
    url = os.environ.get("BRONTO_MCP_URL", "https://mcp.eu.bronto.io/mcp")
    return MCPClient(lambda: streamable_http_client(
        url,
        http_client=httpx2.AsyncClient(headers={"X-BRONTO-API-KEY": api_key}, timeout=60),
    ))
