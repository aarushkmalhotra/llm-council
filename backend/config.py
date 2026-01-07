"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Council members - list of OpenRouter model identifiers (free, high-context)
COUNCIL_MODELS = [
    "google/gemini-2.5-flash-lite",       # keep as requested
    "xiaomi/mimo-v2-flash:free",          # 262K context (free)
    "mistralai/devstral-2512:free",       # 262K context (free)
    "tngtech/deepseek-r1t2-chimera:free", # 164K context (free)
    "nvidia/nemotron-3-nano-30b-a3b:free" # 256K context (free)
]

# Chairman model - synthesizes final response
CHAIRMAN_MODEL = "google/gemini-2.5-flash-lite"

# OpenRouter API endpoint
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
