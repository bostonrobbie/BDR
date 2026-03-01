"""
Structured Logging Configuration - Single setup for all modules.

Call setup_logging() once at application startup. All modules then use:
    import logging
    logger = logging.getLogger(__name__)

Supports two formats:
- "text": Human-readable with timestamps and module names
- "json": Machine-parseable JSON lines for production/aggregation

Usage:
    from src.logging_config import setup_logging
    setup_logging()  # Call once at startup
"""

import json
import logging
import os
import sys
from datetime import datetime


class JSONFormatter(logging.Formatter):
    """Structured JSON log formatter for production use."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
            }

        # Add extra fields if present
        for key in ("contact_id", "batch_id", "agent_name", "run_id",
                     "phase", "action", "duration_ms"):
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)

        return json.dumps(log_entry)


class TextFormatter(logging.Formatter):
    """Human-readable log formatter for development."""

    def __init__(self):
        super().__init__(
            fmt="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )


_initialized = False


def setup_logging(level: str = None, fmt: str = None, log_file: str = None):
    """Configure logging for the entire application.

    Should be called once at startup. Safe to call multiple times (idempotent).

    Args:
        level: Log level override (default: from LOG_LEVEL env var or INFO)
        fmt: Format override ("text" or "json", default: from LOG_FORMAT env var)
        log_file: Log file path override (default: from LOG_FILE env var)
    """
    global _initialized
    if _initialized:
        return
    _initialized = True

    level = level or os.environ.get("LOG_LEVEL", "INFO")
    fmt = fmt or os.environ.get("LOG_FORMAT", "text")
    log_file = log_file or os.environ.get("LOG_FILE", "")

    # Set the root logger level
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove any existing handlers (prevents duplicate output)
    root_logger.handlers.clear()

    # Create formatter
    if fmt == "json":
        formatter = JSONFormatter()
    else:
        formatter = TextFormatter()

    # Console handler (always)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Quiet down noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

    logger = logging.getLogger("bdr")
    logger.info("Logging configured: level=%s, format=%s%s",
                level, fmt, f", file={log_file}" if log_file else "")


def get_agent_logger(agent_name: str) -> logging.Logger:
    """Get a named logger for an agent module.

    Adds the agent_name as an extra field for structured logging.

    Usage:
        logger = get_agent_logger("researcher")
        logger.info("Starting research", extra={"contact_id": "c_123"})
    """
    return logging.getLogger(f"bdr.agents.{agent_name}")
