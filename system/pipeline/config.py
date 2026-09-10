"""Shared config — loads system/.env once, fails fast on missing secrets."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError(
        "OPENAI_API_KEY not set. Copy system/.env.example to system/.env "
        "and fill in your key."
    )

# Chat-model overrides (e.g. DeepSeek). OPENAI_API_KEY is still required: the
# few-shot prompt DB uses OpenAI embeddings regardless of the chat provider.
LLM_MODEL = os.environ.get("LLM_MODEL", "gpt-4o")
LLM_API_KEY = os.environ.get("LLM_API_KEY") or OPENAI_API_KEY
LLM_BASE_URL = os.environ.get("LLM_BASE_URL") or None
