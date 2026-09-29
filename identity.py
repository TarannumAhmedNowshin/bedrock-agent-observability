"""The identity: every .md file in prompts/ becomes part of the system prompt.

Files are joined in alphabetical order, so the file name decides the order.
"""

from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_system_prompt(folder: Path = PROMPTS_DIR) -> str:
    files = sorted(p for p in folder.glob("*.md") if p.is_file())
    return "\n\n".join(p.read_text().strip() for p in files)


SYSTEM_PROMPT = load_system_prompt()
