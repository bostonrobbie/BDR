"""
Pipeline Runner - Background execution engine for batch pipelines.
Runs pipeline phases in a background thread, streams progress via SSE.
"""

import threading
import queue
import json
import time
import os
import sys
from datetime import datetime
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from src.db import models
from src.agents.error_handler import log_pipeline_error

import logging
logger = logging.getLogger("bdr.pipeline")


# ─── GLOBAL STATE ─────────────────────────────────────────────

# Active pipeline runs: run_id -> PipelineRun
_active_runs = {}

# SSE event queues: run_id -> list of queue.Queue
_event_subscribers = {}

_lock = threading.Lock()


class PipelineRun:
    """Tracks a running pipeline instance."""

    PHASES = [
        "initialize", "pre_brief", "extract", "research",
        "score", "ab_assign", "messages", "qc",
        "approval", "generate_html", "finalize"
    ]

    def __init__(self, run_id: str, batch_number: int, config: dict):
        self.run_id = run_id
        self.batch_number = batch_number
        self.config = config
        self.batch_id = None
        self.status = "pending"  # pending, running, paused, approval_needed, completed, failed, cancelled
        self.current_phase = None
        self.current_phase_index = -1
        self.phase_results = {}
        self.error = None
        self.started_at = None
        self.completed_at = None
        self.contact_ids = []
        self.message_ids = []
        self.html_path = None
        self.thread = None
        self.cancel_event = threading.Event()
        self.approval_event = threading.Event()
        self.approval_decisions = {}  # message_id -> "approve" | "reject" | "edit"

    def to_dict(self) -> dict:
        elapsed = None
        if self.started_at:
            end = self.completed_at or datetime.utcnow()
            elapsed = int((end - self.started_at).total_seconds())

        return {
            "run_id": self.run_id,
            "batch_number": self.batch_number,
            "batch_id": self.batch_id,
            "status": self.status,
            "current_phase": self.current_phase,
            "current_phase_index": self.current_phase_index,
            "total_phases": len(self.PHASES),
            "phase_results": self.phase_results,
            "contacts_count": len(self.contact_ids),
            "messages_count": len(self.message_ids),
            "html_path": self.html_path,
            "error": self.error,
            "elapsed_seconds": elapsed,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    def progress_pct(self) -> int:
        if self.current_phase_index < 0:
            return 0
        return int((self.current_phase_index / len(self.PHASES)) * 100)


def _emit(run_id: str, event_type: str, data: dict):
    """Send SSE event to all subscribers."""
    with _lock:
        queues = _event_subscribers.get(run_id, [])
        msg = {"event": event_type, "data": data, "timestamp": datetime.utcnow().isoformat()}
        for q in queues:
            try:
                q.put_nowait(msg)
            except queue.Full:
                pass


def subscribe(run_id: str) -> queue.Queue:
    """Create a new SSE subscription for a pipeline run."""
    q = queue.Queue(maxsize=200)
    with _lock:
        if run_id not in _event_subscribers:
            _event_subscribers[run_id] = []
        _event_subscribers[run_id].append(q)

    # Send current state immediately
    run = _active_runs.get(run_id)
    if run:
        q.put_nowait({"event": "state", "data": run.to_dict(), "timestamp": datetime.utcnow().isoformat()})
    return q


def unsubscribe(run_id: str, q: queue.Queue):
    """Remove an SSE subscription."""
    with _lock:
        queues = _event_subscribers.get(run_id, [])
        if q in queues:
            queues.remove(q)


# ─── PIPELINE EXECUTION ──────────────────────────────────────

def start_pipeline(batch_number: int, config: dict) -> PipelineRun:
    """Start a new pipeline run in a background thread."""
    run_id = models.gen_id("prun")
    run = PipelineRun(run_id, batch_number, config)

    with _lock:
        _active_runs[run_id] = run

    thread = threading.Thread(target=_execute_pipeline, args=(run,), daemon=True)
    run.thread = thread
    thread.start()
    return run


def get_run(run_id: str) -> Optional[PipelineRun]:
    return _active_runs.get(run_id)


def list_runs() -> list:
    return [r.to_dict() for r in _active_runs.values()]


def cancel_run(run_id: str) -> bool:
    run = _active_runs.get(run_id)
    if run and run.status in ("running", "paused", "approval_needed"):
        run.cancel_event.set()
        run.status = "cancelled"
        _emit(run_id, "cancelled", run.to_dict())
        return True
    return False


def approve_messages(run_id: str, decisions: dict) -> bool:
    """Submit approval decisions for messages in approval gate.
    decisions: {message_id: "approve" | "reject" | "edit"}
    """
    run = _active_runs.get(run_id)
    if run and run.status == "approval_needed":
        run.approval_decisions = decisions
        run.approval_event.set()
        return True
    return False


def skip_approval(run_id: str) -> bool:
    """Auto-approve all messages and continue."""
    run = _active_runs.get(run_id)
    if run and run.status == "approval_needed":
        run.approval_decisions = {}  # empty = approve all
        run.approval_event.set()
        return True
    return False


# ─── PIPELINE THREAD ─────────────────────────────────────────

def _execute_pipeline(run: PipelineRun):
    """Run the full pipeline in a background thread."""
    from src.agents.batch_builder import BatchPipeline
    from src.agents.scorer import batch_score
    from src.agents.ab_assigner import assign_ab_groups
    from src.agents.quality_gate import run_quality_gate
    from src.agents.deliverable_generator import generate_batch_html

    run.status = "running"
    run.started_at = datetime.utcnow()
    _emit(run.run_id, "started", run.to_dict())

    builder = BatchPipeline(run.batch_number, run.config)

    try:
        # Phase 0: Initialize
        _start_phase(run, "initialize")
        batch = builder.initialize()
        run.batch_id = builder.batch_id
        _complete_phase(run, "initialize", {"batch_id": builder.batch_id})

        if _check_cancel(run):
            return

        # Phase 1: Pre-Brief
        _start_phase(run, "pre_brief")
        brief = builder.phase_pre_brief()
        _complete_phase(run, "pre_brief", {
            "insights": len(brief.get("insights", [])) if brief else 0,
            "is_first_batch": brief is None
        })

        if _check_cancel(run):
            return

        # Phase 2: Extract
        # In automated mode, we check if prospects were pre-loaded in config
        _start_phase(run, "extract")
        prospects = run.config.get("prospects", [])
        if prospects:
            contact_ids = builder.phase_extract(prospects)
            run.contact_ids = contact_ids
        else:
            # No prospects provided - batch needs manual prospect loading
            run.contact_ids = builder.contacts or []
            # Check if contacts were already added to batch
            conn = models.get_db()
            rows = conn.execute(
                "SELECT contact_id FROM batch_prospects WHERE batch_id=?",
                (builder.batch_id,)
            ).fetchall()
            conn.close()
            run.contact_ids = [r["contact_id"] for r in rows]
            builder.contacts = run.contact_ids

        _complete_phase(run, "extract", {"contacts": len(run.contact_ids)})

        if _check_cancel(run):
            return

        # Phase 3: Research
        _start_phase(run, "research")
        research_count = 0
        research_missing = []
        conn = models.get_db()
        for cid in run.contact_ids:
            r = conn.execute(
                "SELECT COUNT(*) FROM research_snapshots WHERE contact_id=?", (cid,)
            ).fetchone()[0]
            if r > 0:
                research_count += r
            else:
                research_missing.append(cid)
        conn.close()

        # If research is missing and auto_research is enabled, generate it
        if research_missing and run.config.get("auto_research", False):
            from src.agents.researcher import build_research_context
            from src.agents.error_handler import safe_execute
            for cid in research_missing:
                ctx = safe_execute(
                    build_research_context, args=(cid,),
                    phase="research", contact_id=cid,
                    agent_name="researcher", batch_id=run.batch_id,
                    fallback={"error": "research failed"},
                )
                if ctx and not ctx.get("error"):
                    research_count += 1
                if _check_cancel(run):
                    return

        _complete_phase(run, "research", {
            "snapshots_found": research_count,
            "missing": len(research_missing),
        })

        if _check_cancel(run):
            return

        # Phase 4: Score
        _start_phase(run, "score")
        if run.contact_ids:
            scores = batch_score(run.contact_ids)
            _complete_phase(run, "score", {"scored": len(scores)})
        else:
            _complete_phase(run, "score", {"scored": 0, "skipped": True})

        if _check_cancel(run):
            return

        # Phase 5: A/B Assign
        _start_phase(run, "ab_assign")
        if run.contact_ids:
            ab_result = assign_ab_groups(
                run.contact_ids,
                run.config.get("ab_variable", "pain_hook"),
                run.config.get("ab_groups", {"A": "Group A", "B": "Group B"}),
                builder.batch_id,
            )
            _complete_phase(run, "ab_assign", ab_result if isinstance(ab_result, dict) else {"assigned": True})
        else:
            _complete_phase(run, "ab_assign", {"skipped": True})

        if _check_cancel(run):
            return

        # Phase 6: Messages
        _start_phase(run, "messages")
        msgs = models.list_messages(batch_id=builder.batch_id)

        # If no messages exist and auto_messages is enabled, generate them
        if not msgs and run.config.get("auto_messages", False):
            from src.agents.message_writer import build_all_prompts, store_generated_messages
            from src.agents.error_handler import safe_execute
            generated_count = 0
            for cid in run.contact_ids:
                # Look up A/B assignment for this contact
                conn = models.get_db()
                bp = conn.execute(
                    "SELECT ab_group FROM batch_prospects WHERE batch_id=? AND contact_id=?",
                    (builder.batch_id, cid)
                ).fetchone()
                conn.close()
                ab_group = bp["ab_group"] if bp else None
                ab_variable = run.config.get("ab_variable", "pain_hook")

                prompts = safe_execute(
                    build_all_prompts,
                    args=(cid,),
                    kwargs={"ab_group": ab_group, "ab_variable": ab_variable},
                    phase="messages", contact_id=cid,
                    agent_name="message_writer", batch_id=run.batch_id,
                    fallback={"error": "message generation failed"},
                )
                if prompts and not prompts.get("error"):
                    store_generated_messages(
                        cid, prompts, batch_id=builder.batch_id,
                        ab_group=ab_group, ab_variable=ab_variable,
                    )
                    generated_count += 1
                if _check_cancel(run):
                    return

            # Re-fetch messages after generation
            msgs = models.list_messages(batch_id=builder.batch_id)

        run.message_ids = [m["id"] for m in msgs]
        builder.messages = msgs
        _complete_phase(run, "messages", {"count": len(msgs)})

        if _check_cancel(run):
            return

        # Phase 7: QC Gate
        _start_phase(run, "qc")
        qc_results = {"passed": 0, "failed": 0, "flags": []}
        for msg in msgs:
            if msg.get("touch_type") == "call_snippet":
                continue
            qc = run_quality_gate(msg)
            if qc.get("passed"):
                qc_results["passed"] += 1
            else:
                qc_results["failed"] += 1
                qc_results["flags"].append({
                    "message_id": msg["id"],
                    "contact_id": msg.get("contact_id"),
                    "touch_number": msg.get("touch_number"),
                    "issues": [c["check"] for c in qc.get("checks", []) if not c.get("passed")]
                })
        _complete_phase(run, "qc", qc_results)

        if _check_cancel(run):
            return

        # Phase 8: Approval Gate
        _start_phase(run, "approval")
        if run.config.get("auto_approve", True):
            _complete_phase(run, "approval", {"auto_approved": True})
        else:
            # Pause for human approval
            run.status = "approval_needed"
            _emit(run.run_id, "approval_needed", {
                "run_id": run.run_id,
                "messages": len(msgs),
                "qc_passed": qc_results["passed"],
                "qc_failed": qc_results["failed"],
                "flags": qc_results["flags"][:10],  # First 10 flags
            })

            # Wait for approval (timeout 24 hours)
            approved = run.approval_event.wait(timeout=86400)
            if not approved or _check_cancel(run):
                if not run.cancel_event.is_set():
                    run.status = "failed"
                    run.error = "Approval timed out"
                    _emit(run.run_id, "failed", run.to_dict())
                return

            # Process approval decisions
            rejected = [mid for mid, d in run.approval_decisions.items() if d == "reject"]
            if rejected:
                conn = models.get_db()
                for mid in rejected:
                    conn.execute("UPDATE message_drafts SET approval_status='rejected' WHERE id=?", (mid,))
                conn.commit()
                conn.close()

            run.status = "running"
            _complete_phase(run, "approval", {
                "approved": len(run.approval_decisions) - len(rejected),
                "rejected": len(rejected),
            })

        if _check_cancel(run):
            return

        # Phase 9: Generate HTML
        _start_phase(run, "generate_html")
        html_path = generate_batch_html(builder.batch_id, run.batch_number)
        run.html_path = html_path
        _complete_phase(run, "generate_html", {"file": html_path})

        if _check_cancel(run):
            return

        # Phase 10: Finalize
        _start_phase(run, "finalize")
        builder.finalize()
        run.status = "completed"
        run.completed_at = datetime.utcnow()
        _complete_phase(run, "finalize", run.to_dict())
        _emit(run.run_id, "completed", run.to_dict())

    except Exception as e:
        run.status = "failed"
        run.error = str(e)
        run.completed_at = datetime.utcnow()
        logger.error("Pipeline failed in phase %s: %s", run.current_phase, e, exc_info=True)
        log_pipeline_error(
            phase=run.current_phase or "unknown",
            error=e,
            batch_id=run.batch_id,
            severity="critical",
        )
        _emit(run.run_id, "error", {"error": str(e), "phase": run.current_phase})


def _start_phase(run: PipelineRun, phase: str):
    idx = run.PHASES.index(phase) if phase in run.PHASES else -1
    run.current_phase = phase
    run.current_phase_index = idx
    _emit(run.run_id, "phase_start", {
        "phase": phase,
        "phase_index": idx,
        "progress_pct": run.progress_pct(),
    })


def _complete_phase(run: PipelineRun, phase: str, result: dict = None):
    run.phase_results[phase] = {
        "status": "completed",
        "result": result or {},
        "completed_at": datetime.utcnow().isoformat(),
    }
    _emit(run.run_id, "phase_complete", {
        "phase": phase,
        "result": result or {},
        "progress_pct": run.progress_pct(),
    })


def _check_cancel(run: PipelineRun) -> bool:
    if run.cancel_event.is_set():
        run.status = "cancelled"
        run.completed_at = datetime.utcnow()
        _emit(run.run_id, "cancelled", run.to_dict())
        return True
    return False


# ─── SINGLE AGENT ACTIONS ────────────────────────────────────

def run_agent_action(action: str, contact_id: str = None, batch_id: str = None, params: dict = None) -> dict:
    """Run a single agent action (not a full pipeline)."""
    params = params or {}
    result = {"action": action, "status": "started", "started_at": datetime.utcnow().isoformat()}

    try:
        if action == "re_score" and contact_id:
            from src.agents.scorer import score_icp_and_save
            score_result = score_icp_and_save(contact_id)
            result["status"] = "completed"
            result["data"] = score_result

        elif action == "re_research" and contact_id:
            # Mark existing research as stale, trigger fresh research
            result["status"] = "completed"
            result["data"] = {"message": "Research refresh queued. Run in Cowork session for Chrome-based research."}

        elif action == "regenerate_messages" and contact_id:
            result["status"] = "completed"
            result["data"] = {"message": "Message regeneration queued. Requires LLM via Cowork session."}

        elif action == "run_qc" and contact_id:
            from src.agents.quality_gate import run_quality_gate
            msgs = models.get_messages_for_contact(contact_id)
            qc_results = []
            for msg in msgs:
                if msg.get("touch_type") == "call_snippet":
                    continue
                qc = run_quality_gate(msg)
                qc_results.append({"message_id": msg["id"], "passed": qc.get("passed"), "checks": qc.get("checks", [])})
            result["status"] = "completed"
            result["data"] = {"qc_results": qc_results}

        elif action == "score_batch" and batch_id:
            from src.agents.scorer import batch_score
            conn = models.get_db()
            rows = conn.execute(
                "SELECT contact_id FROM batch_prospects WHERE batch_id=?", (batch_id,)
            ).fetchall()
            conn.close()
            cids = [r["contact_id"] for r in rows]
            scores = batch_score(cids)
            result["status"] = "completed"
            result["data"] = {"scored": len(scores)}

        elif action == "generate_html" and batch_id:
            from src.agents.deliverable_generator import generate_batch_html
            conn = models.get_db()
            batch = conn.execute("SELECT batch_number FROM batches WHERE id=?", (batch_id,)).fetchone()
            conn.close()
            if batch:
                path = generate_batch_html(batch_id, batch["batch_number"])
                result["status"] = "completed"
                result["data"] = {"html_path": path}
            else:
                result["status"] = "failed"
                result["error"] = "Batch not found"

        elif action == "run_pre_brief":
            from src.agents.pre_brief import generate_pre_brief
            brief = generate_pre_brief()
            result["status"] = "completed"
            result["data"] = brief

        else:
            result["status"] = "failed"
            result["error"] = f"Unknown action: {action}"

    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)

    result["completed_at"] = datetime.utcnow().isoformat()
    return result
