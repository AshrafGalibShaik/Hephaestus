"""
Configuration manager for Hephaestus.
Stores user preferences in ~/.hephaestus/config.json
"""

import os
import json

CONFIG_DIR = os.path.expanduser("~/.hephaestus")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

SUPPORTED_MODELS = {
    "1": {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash", "provider": "google", "key_env": "GOOGLE_API_KEY"},
    "2": {"id": "gemini-2.0-flash", "name": "Gemini 2.0 Flash", "provider": "google", "key_env": "GOOGLE_API_KEY"},
    "3": {"id": "gemini-1.5-flash", "name": "Gemini 1.5 Flash", "provider": "google", "key_env": "GOOGLE_API_KEY"},
    "4": {"id": "gpt-4o", "name": "GPT-4o", "provider": "openai", "key_env": "OPENAI_API_KEY"},
    "5": {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "openai", "key_env": "OPENAI_API_KEY"},
    "6": {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "openai", "key_env": "OPENAI_API_KEY"},
}

def load_config():
    """Load config from disk. Returns empty dict if not found."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_config(config):
    """Save config to disk."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def is_configured():
    """Check if the first-run setup has been completed."""
    config = load_config()
    return config.get("model_id") and config.get("api_key")

def get_model_config():
    """Get the current model configuration."""
    return load_config()
