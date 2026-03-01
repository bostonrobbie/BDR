"""
Agent Error Handler - Captures and logs non-fatal pipeline errors.

Instead of silently catching exceptions, agents call log_pipeline_error()
to record what went wrong. Errors are stored in the pipeline_errors table
and surfaced in deliverables so Rob knows what to check.

Usage:
    from src.agents.error_handler import log_pipeline_error, safe_execute

    # Option 1: Manual logging
    try:
        result = risky_operation()
    except Exception as e:
        log_pipeline_error(phase="research", error=e, contact_id=cid)
        result = fallback_value

    # Option 2: Safe execution wrapper
    result = safe_execute(
        risky_operation, args=(arg1, arg2),
        phase="scoring", contact_id=cid,
        fallback=default_value
    )
"""

import json
import logging
import traceback
from datetime import datetime
from typing import Any, Callable, Optional

logger = logging.getLogger("bdr.error_handler")


def log_pipeline_error(
    phase: str,
    error: Exception = None,
    error_message: str = None,
    batch_id: str = None,
    contact_id: str = None,
    agent_name: str = None,
    context: dict = None,
    severity: str = "warning",
):
    """Log a non-fatal pipeline error to the database and logger.

    Args:
        phase: Pipeline phase where the error occurred (research, scoring, messages, etc.)
        error: The exception object (optional if error_message provided)
        error_message: Human-readable error description
        batch_id: Associated batch ID
        contact_id: Associated contact ID
        agent_name: Which agent encountered the error
        context: Additional context dict
        severity: "warning", "error", or "critical"
    """
    msg = error_message or (str(error) if error else "Unknown error")
    error_type = type(error).__name__ if error else "UnknownError"

    # Log to Python logger
    log_extra = {
        "phase": phase,
        "agent_name": agent_name or "",
        "contact_id": contact_id or "",
        "batch_id": batch_id or "",
    }

    if severity == "critical":
        logger.critical("Pipeline error in %s: %s", phase, msg, extra=log_extra)
    elif severity == "error":
        logger.error("Pipeline error in %s: %s", phase, msg, extra=log_extra)
    else:
        logger.warning("Pipeline error in %s: %s", phase, msg, extra=log_extra)

    # Log to database
    try:
        from src.db import models
        conn = models.get_db()
        conn.execute("""
            INSERT INTO pipeline_errors
                (batch_id, contact_id, phase, agent_name, error_type,
                 error_message, context, severity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            batch_id, contact_id, phase, agent_name,
            error_type, msg, json.dumps(context or {}), severity,
        ))
        conn.commit()
        conn.close()
    except Exception as db_err:
        # If we can't even log the error to the DB, log to stderr
        logger.error("Failed to log pipeline error to DB: %s", db_err)


def safe_execute(
    fn: Callable,
    args: tuple = (),
    kwargs: dict = None,
    phase: str = "unknown",
    agent_name: str = None,
    batch_id: str = None,
    contact_id: str = None,
    fallback: Any = None,
    severity: str = "warning",
) -> Any:
    """Execute a function with automatic error capture.

    If the function raises, the error is logged and the fallback value is returned.
    Use this for operations that should not crash the pipeline.

    Args:
        fn: The function to call.
        args: Positional arguments.
        kwargs: Keyword arguments.
        phase: Pipeline phase name.
        agent_name: Agent name for logging.
        batch_id: Associated batch ID.
        contact_id: Associated contact ID.
        fallback: Value to return if fn raises.
        severity: Error severity level.

    Returns:
        The function's return value, or fallback if it raised.
    """
    kwargs = kwargs or {}
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        log_pipeline_error(
            phase=phase,
            error=e,
            batch_id=batch_id,
            contact_id=contact_id,
            agent_name=agent_name,
            context={"function": fn.__name__, "traceback": traceback.format_exc()[-500:]},
            severity=severity,
        )
        return fallback


def get_errors(batch_id: str = None, severity: str = None,
               unresolved_only: bool = True) -> list:
    """Get pipeline errors, optionally filtered.

    Returns list of error dicts.
    """
    try:
        from src.db import models
        conn = models.get_db()
        query = "SELECT * FROM pipeline_errors WHERE 1=1"
        params = []

        if batch_id:
            query += " AND batch_id=?"
            params.append(batch_id)
        if severity:
            query += " AND severity=?"
            params.append(severity)
        if unresolved_only:
            query += " AND resolved=0"

        query += " ORDER BY created_at DESC"
        rows = conn.execute(query, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


def resolve_error(error_id: int):
    """Mark a pipeline error as resolved."""
    try:
        from src.db import models
        conn = models.get_db()
        conn.execute("UPDATE pipeline_errors SET resolved=1 WHERE id=?", (error_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.error("Failed to resolve error %s: %s", error_id, e)
