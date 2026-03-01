"""
Centralized Configuration - Single source of truth for all settings.

All environment variables are read here, validated, and exposed as module-level
constants. Other modules import from here instead of reading os.environ directly.

Usage:
    from src.config import DB_PATH, OLLAMA_HOST, LOG_LEVEL
"""

import os
import sys

# ─── PATHS ───────────────────────────────────────────────────

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_ROOT = os.path.join(PROJECT_ROOT, "memory")
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")

# ─── DATABASE ────────────────────────────────────────────────

DB_PATH = os.environ.get("OCC_DB_PATH", os.path.join(PROJECT_ROOT, "outreach.db"))
DB_JOURNAL_MODE = os.environ.get("OCC_JOURNAL_MODE", "WAL")

# ─── LLM ─────────────────────────────────────────────────────

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT_SECONDS", "120"))
LLM_FALLBACK_PROVIDER = os.environ.get("LLM_FALLBACK_PROVIDER", "")

# ─── API ─────────────────────────────────────────────────────

API_HOST = os.environ.get("API_HOST", "0.0.0.0")
API_PORT = int(os.environ.get("API_PORT", "8000"))
API_WORKERS = int(os.environ.get("API_WORKERS", "1"))

# ─── PIPELINE ────────────────────────────────────────────────

PIPELINE_MAX_WORKERS = int(os.environ.get("PIPELINE_MAX_WORKERS", "3"))
PIPELINE_AUTO_APPROVE = os.environ.get("PIPELINE_AUTO_APPROVE", "true").lower() == "true"

# ─── LOGGING ─────────────────────────────────────────────────

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.environ.get("LOG_FORMAT", "text")  # "text" or "json"
LOG_FILE = os.environ.get("LOG_FILE", "")  # empty = stdout only

# ─── FEATURE FLAGS ───────────────────────────────────────────

ENABLE_MEMORY_LAYER = os.environ.get("ENABLE_MEMORY_LAYER", "true").lower() == "true"
ENABLE_FILE_WATCHER = os.environ.get("ENABLE_FILE_WATCHER", "false").lower() == "true"

# ─── VALIDATION ──────────────────────────────────────────────

_VALID_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
_VALID_LOG_FORMATS = {"text", "json"}
_VALID_JOURNAL_MODES = {"WAL", "DELETE", "MEMORY", "OFF"}

_errors = []

if LOG_LEVEL not in _VALID_LOG_LEVELS:
    _errors.append(f"LOG_LEVEL must be one of {_VALID_LOG_LEVELS}, got '{LOG_LEVEL}'")

if LOG_FORMAT not in _VALID_LOG_FORMATS:
    _errors.append(f"LOG_FORMAT must be one of {_VALID_LOG_FORMATS}, got '{LOG_FORMAT}'")

if DB_JOURNAL_MODE not in _VALID_JOURNAL_MODES:
    _errors.append(f"OCC_JOURNAL_MODE must be one of {_VALID_JOURNAL_MODES}, got '{DB_JOURNAL_MODE}'")

if OLLAMA_TIMEOUT < 1:
    _errors.append(f"OLLAMA_TIMEOUT_SECONDS must be positive, got {OLLAMA_TIMEOUT}")

if PIPELINE_MAX_WORKERS < 1:
    _errors.append(f"PIPELINE_MAX_WORKERS must be positive, got {PIPELINE_MAX_WORKERS}")

if _errors:
    for e in _errors:
        print(f"[config] ERROR: {e}", file=sys.stderr)
    # Don't crash during import - agents may not need all config
    # But print warnings so they're visible


def validate(strict: bool = False) -> list:
    """Validate all configuration settings.

    Args:
        strict: If True, raise ValueError on any errors.

    Returns:
        List of error messages (empty if all valid).
    """
    if strict and _errors:
        raise ValueError(f"Configuration errors: {'; '.join(_errors)}")
    return list(_errors)


def print_config():
    """Print current configuration (safe - no secrets)."""
    print("=" * 50)
    print("BDR Configuration")
    print("=" * 50)
    print(f"  DB_PATH:              {DB_PATH}")
    print(f"  DB_JOURNAL_MODE:      {DB_JOURNAL_MODE}")
    print(f"  OLLAMA_HOST:          {OLLAMA_HOST}")
    print(f"  OLLAMA_MODEL:         {OLLAMA_MODEL}")
    print(f"  OLLAMA_TIMEOUT:       {OLLAMA_TIMEOUT}s")
    print(f"  API_HOST:             {API_HOST}")
    print(f"  API_PORT:             {API_PORT}")
    print(f"  LOG_LEVEL:            {LOG_LEVEL}")
    print(f"  LOG_FORMAT:           {LOG_FORMAT}")
    print(f"  PIPELINE_MAX_WORKERS: {PIPELINE_MAX_WORKERS}")
    print(f"  PIPELINE_AUTO_APPROVE:{PIPELINE_AUTO_APPROVE}")
    print(f"  ENABLE_MEMORY_LAYER:  {ENABLE_MEMORY_LAYER}")
    print(f"  ENABLE_FILE_WATCHER:  {ENABLE_FILE_WATCHER}")
    print(f"  PROJECT_ROOT:         {PROJECT_ROOT}")
    print("=" * 50)
