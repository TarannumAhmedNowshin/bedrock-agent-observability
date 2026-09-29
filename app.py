"""Shared plumbing: the model, the HTTP app, and answer cleanup.

BedrockAgentCoreApp gives us the contract AgentCore expects:
POST /invocations and GET /ping on port 8080.
"""

import os
import re

from bedrock_agentcore import BedrockAgentCoreApp
from strands.models import BedrockModel

MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0")
REGION = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION") or "us-west-2"

model = BedrockModel(model_id=MODEL_ID, region_name=REGION)
app = BedrockAgentCoreApp()


def answer(result, reasoning: bool = False) -> str:
    """Some models write their reasoning into the answer. Drop it unless asked."""
    text = str(result).strip()
    if reasoning or not text.startswith("<reasoning>"):
        return text
    if re.search(r"</(reasoning|analysis)>?", text):  # closed: cut at the last close tag
        return re.sub(r"(?s)^.*</(reasoning|analysis)>?", "", text).strip()
    m = re.search(r"(?m)^(\*\*|#|\|)", text)          # unclosed: cut where the answer starts
    return text[m.start():].strip() if m else text
