"""Configuration for the LLM Council."""

import os
import json
from typing import List

# Optional: load variables from a local .env during local development.
# In environments like Google Colab, python-dotenv may not be installed.
try:
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except Exception:
    pass

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Defaults: council members (free, high-context)
_DEFAULT_COUNCIL_MODELS: List[str] = [
    "google/gemini-2.5-flash-lite",       # keep as requested
    "xiaomi/mimo-v2-flash:free",          # 262K context (free)
    "mistralai/devstral-2512:free",       # 262K context (free)
    "tngtech/deepseek-r1t2-chimera:free", # 164K context (free)
    "nvidia/nemotron-3-nano-30b-a3b:free" # 256K context (free)
]

def _parse_models_env(value: str) -> List[str]:
    """Parse a models list from an env var.

    Accepts either:
    - JSON list: '["model/a", "model/b"]'
    - Comma-separated: 'model/a, model/b'
    """
    value = value.strip()
    if not value:
        return []

    if value.startswith('['):
        parsed = json.loads(value)
        if not isinstance(parsed, list) or not all(isinstance(x, str) for x in parsed):
            raise ValueError("LLM_COUNCIL_MODELS must be a JSON list of strings")
        return [m.strip() for m in parsed if m.strip()]

    return [part.strip() for part in value.split(',') if part.strip()]


# Council members - overridable via env var `LLM_COUNCIL_MODELS`
_models_env = os.getenv("LLM_COUNCIL_MODELS")
COUNCIL_MODELS = _parse_models_env(_models_env) if _models_env else _DEFAULT_COUNCIL_MODELS

# Chairman model - synthesizes final response (overridable via env var `LLM_COUNCIL_CHAIRMAN_MODEL`)
CHAIRMAN_MODEL = os.getenv("LLM_COUNCIL_CHAIRMAN_MODEL") or "google/gemini-2.5-flash-lite"

# OpenRouter API endpoint
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL") or "https://openrouter.ai/api/v1/chat/completions"

def _resolve_data_dir() -> str:
    """Resolve the directory used to store conversation JSON files.

    Priority:
    1) LLM_COUNCIL_DATA_DIR env var (explicit override)
    2) If running in Colab and Google Drive is mounted, store under MyDrive
    3) Fallback to local repo directory (existing behavior)
    """
    env_dir = os.getenv("LLM_COUNCIL_DATA_DIR")
    if env_dir:
        return env_dir

    # Auto-detect Google Colab Drive mount.
    # The mount point exists only after the user runs drive.mount('/content/drive').
    drive_root = "/content/drive/MyDrive"
    if os.path.isdir(drive_root):
        return os.path.join(drive_root, "llm-council", "data", "conversations")

    return "data/conversations"


# Data directory for conversation storage
DATA_DIR = _resolve_data_dir()
