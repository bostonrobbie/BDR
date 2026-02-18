"""
Swarm Supervisor - Orchestrates multi-agent parallel processing.
Coordinates research, drafting, QA, and sequencing across a batch of prospects.

Safety controls:
- Hard cap on parallelism (max_workers)
- Dedupe keys prevent duplicate tasks
- All outputs must reference stored research (no fabrication)
- If research is missing, agent flags it rather than inventing
- Feature flags control enablement
- Every run is logged and auditable
"""

import sys
import os
import uuid
import json
import time
import logging
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Optional, Callable

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models

logger = logging.getLogger("swarm_supervisor")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(levelname)s: %(message)s")


# ─── CONFIGURATION ─────────────────────────────────────────────

DEFAULT_CONFIG = {
    "max_workers": 3,           # Max parallel agent threads
    "max_tasks_per_run": 200,   # Hard cap on total tasks per swarm run
    "task_timeout_seconds": 120, # Per-task timeout
    "retry_max": 2,             # Max retries per task
    "channels": ["linkedin", "email"],  # Which channels to draft for
    "require_research": True,   # Block drafting if research is missing
    "qc_blocking": True,        # Block approval if QC fails
}


class SwarmSupervisor:
    """Orchestrates parallel agent processing for a batch of prospects."""
    
    def __init__(self, config: dict = None):
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.run_id = None
        self.cancelled = False
        self._progress_callbacks = []
    
    def on_progress(self, callback: Callable):
        """Register a progress callback."""
        self._progress_callbacks.append(callback)
    
    def _emit(self, event_type: str, data: dict):
        """Emit progress event to all registered callbacks."""
        for cb in self._progress_callbacks:
            try:
                cb(event_type, data)
            except Exception:
                pass
    
    def run_batch(self, contact_ids: List[str], batch_id: str = None) -> dict:
        """Run the full swarm pipeline for a list of contacts."""
        
        # Check feature flag
        if not models.is_feature_enabled("agent_swarm"):
            return {"error": "Agent swarm is disabled via feature flag"}
        
        # Create swarm run
        swarm_run = models.create_swarm_run(
            swarm_type="batch_process",
            batch_id=batch_id,
            config=self.config,
        )
        self.run_id = swarm_run["id"]
        
        logger.info(f"Swarm run {self.run_id} started for {len(contact_ids)} contacts")
        self._emit("swarm_started", {"run_id": self.run_id, "total_contacts": len(contact_ids)})
        
        results = {
            "run_id": self.run_id,
            "total_contacts": len(contact_ids),
            "phases": {},
            "errors": [],
        }
        
        try:
            # Phase 1: Research (parallel)
            research_results = self._run_phase("research", contact_ids)
            results["phases"]["research"] = research_results
            
            if self.cancelled:
                self._finalize("cancelled", results)
                return results
            
            # Phase 2: Draft messages (parallel, depends on research)
            researched_ids = [cid for cid, r in research_results.items() if r.get("status") == "completed"]
            draft_results = self._run_phase("draft", researched_ids)
            results["phases"]["draft"] = draft_results
            
            if self.cancelled:
                self._finalize("cancelled", results)
                return results
            
            # Phase 3: QA check (parallel, depends on drafts)
            drafted_ids = [cid for cid, r in draft_results.items() if r.get("status") == "completed"]
            qa_results = self._run_phase("qa", drafted_ids)
            results["phases"]["qa"] = qa_results
            
            if self.cancelled:
                self._finalize("cancelled", results)
                return results
            
            # Phase 4: Sequence planning (parallel)
            qa_passed_ids = [cid for cid, r in qa_results.items() if r.get("passed")]
            sequence_results = self._run_phase("sequence", qa_passed_ids)
            results["phases"]["sequence"] = sequence_results
            
            # Finalize
            self._finalize("completed", results)
            
        except Exception as e:
            logger.error(f"Swarm run {self.run_id} failed: {e}")
            results["errors"].append(str(e))
            self._finalize("error", results)
        
        return results
    
    def _run_phase(self, phase_name: str, contact_ids: List[str]) -> dict:
        """Run a single phase across all contacts with bounded parallelism."""
        logger.info(f"Phase '{phase_name}' starting for {len(contact_ids)} contacts")
        self._emit("phase_started", {"phase": phase_name, "count": len(contact_ids)})
        
        results = {}
        max_workers = min(self.config["max_workers"], len(contact_ids) or 1)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_cid = {}
            for cid in contact_ids:
                if self.cancelled:
                    break
                
                # Create task with dedupe
                task = models.create_swarm_task({
                    "swarm_run_id": self.run_id,
                    "agent_name": f"{phase_name}_agent",
                    "task_type": phase_name,
                    "contact_id": cid,
                    "input_data": {"contact_id": cid, "phase": phase_name},
                })
                
                if task.get("duplicate"):
                    logger.info(f"Skipping duplicate task for {cid} in phase {phase_name}")
                    results[cid] = {"status": "skipped", "reason": "duplicate"}
                    continue
                
                future = executor.submit(self._execute_task, phase_name, cid, task["id"])
                future_to_cid[future] = (cid, task["id"])
            
            for future in as_completed(future_to_cid):
                cid, task_id = future_to_cid[future]
                try:
                    result = future.result(timeout=self.config["task_timeout_seconds"])
                    results[cid] = result
                    
                    # Update task
                    models.update_swarm_task(task_id, {
                        "status": "completed" if result.get("status") == "completed" else "error",
                        "output_data": result,
                        "completed_at": datetime.utcnow().isoformat(),
                    })
                    
                except Exception as e:
                    logger.error(f"Task failed for {cid} in {phase_name}: {e}")
                    results[cid] = {"status": "error", "error": str(e)}
                    models.update_swarm_task(task_id, {
                        "status": "error",
                        "error_message": str(e),
                        "completed_at": datetime.utcnow().isoformat(),
                    })
                
                self._emit("task_completed", {
                    "phase": phase_name,
                    "contact_id": cid,
                    "status": results[cid].get("status", "unknown"),
                })
        
        # Update swarm run progress
        completed = sum(1 for r in results.values() if r.get("status") == "completed")
        failed = sum(1 for r in results.values() if r.get("status") == "error")
        swarm = models.get_swarm_run(self.run_id)
        models.update_swarm_run(self.run_id, {
            "completed_tasks": swarm.get("completed_tasks", 0) + completed,
            "failed_tasks": swarm.get("failed_tasks", 0) + failed,
        })
        
        self._emit("phase_completed", {"phase": phase_name, "completed": completed, "failed": failed})
        logger.info(f"Phase '{phase_name}' done: {completed} completed, {failed} failed")
        
        return results
    
    def _execute_task(self, phase_name: str, contact_id: str, task_id: str) -> dict:
        """Execute a single agent task. Dispatches to the appropriate agent."""
        
        models.update_swarm_task(task_id, {
            "status": "running",
            "started_at": datetime.utcnow().isoformat(),
        })
        
        # Start an agent_run for tracing
        agent_run = models.start_agent_run(
            run_type=phase_name,
            agent_name=f"swarm_{phase_name}_agent",
            contact_id=contact_id,
        )
        
        try:
            if phase_name == "research":
                result = self._research_task(contact_id)
            elif phase_name == "draft":
                result = self._draft_task(contact_id)
            elif phase_name == "qa":
                result = self._qa_task(contact_id)
            elif phase_name == "sequence":
                result = self._sequence_task(contact_id)
            else:
                result = {"status": "error", "error": f"Unknown phase: {phase_name}"}
            
            models.complete_agent_run(agent_run["id"], outputs=result)
            return result
            
        except Exception as e:
            models.complete_agent_run(agent_run["id"], outputs={}, error=str(e))
            raise
    
    def _research_task(self, contact_id: str) -> dict:
        """Research agent: check for existing research, compile brief."""
        contact = models.get_contact(contact_id)
        if not contact:
            return {"status": "error", "error": "Contact not found"}
        
        # Check for existing research
        conn = models.get_db()
        existing = conn.execute("""
            SELECT * FROM research_snapshots
            WHERE contact_id=? ORDER BY created_at DESC LIMIT 1
        """, (contact_id,)).fetchone()
        conn.close()
        
        if existing:
            research = dict(existing)
            return {
                "status": "completed",
                "research_id": research["id"],
                "source": "cached",
                "headline": research.get("headline", ""),
                "has_company_research": bool(research.get("company_news") or research.get("company_products")),
            }
        
        # No existing research, flag for manual research
        return {
            "status": "completed",
            "research_id": None,
            "source": "needs_research",
            "flag": "Research missing for this contact. Queue for manual research via Chrome/LinkedIn.",
            "contact_name": f"{contact.get('first_name', '')} {contact.get('last_name', '')}",
        }
    
    def _draft_task(self, contact_id: str) -> dict:
        """Writer agent: generate email and LinkedIn drafts from research."""
        contact = models.get_contact(contact_id)
        if not contact:
            return {"status": "error", "error": "Contact not found"}
        
        # Check research exists
        conn = models.get_db()
        research = conn.execute("""
            SELECT * FROM research_snapshots
            WHERE contact_id=? ORDER BY created_at DESC LIMIT 1
        """, (contact_id,)).fetchone()
        conn.close()
        
        if not research and self.config.get("require_research"):
            return {
                "status": "error",
                "error": "Research required before drafting. Flag contact for research first.",
            }
        
        research_data = dict(research) if research else {}
        
        # Check suppression before email drafts
        email = contact.get("email")
        email_suppressed = False
        if email and models.is_feature_enabled("suppression_check"):
            email_suppressed = models.is_suppressed(email)
        
        drafts_created = []
        channels = self.config.get("channels", ["linkedin", "email"])
        
        for channel in channels:
            if channel == "email" and (email_suppressed or not email):
                continue
            
            # Check if draft already exists for this contact+channel
            existing = models.get_messages_for_contact(contact_id)
            contact_existing = [m for m in existing if m.get("channel") == channel]
            
            if contact_existing:
                drafts_created.append({
                    "channel": channel,
                    "action": "skipped",
                    "reason": "drafts already exist",
                })
                continue
            
            # Create placeholder draft (actual LLM generation happens in Cowork session)
            for touch_num in [1, 3, 5, 6] if channel == "email" else [1, 3, 6]:
                touch_types = {1: "inmail" if channel == "linkedin" else "email",
                               3: "inmail" if channel == "linkedin" else "email",
                               5: "email", 6: "breakup"}
                
                draft = models.create_message_draft({
                    "contact_id": contact_id,
                    "channel": channel,
                    "touch_number": touch_num,
                    "touch_type": touch_types.get(touch_num, channel),
                    "subject_line": f"[DRAFT] Touch {touch_num} for {contact.get('first_name', '')}",
                    "body": f"[PENDING LLM GENERATION] Research-based {channel} message for "
                            f"{contact.get('first_name', '')} {contact.get('last_name', '')} "
                            f"at {contact.get('company_name', 'their company')}. "
                            f"Research headline: {research_data.get('headline', 'N/A')}",
                    "word_count": 0,
                    "approval_status": "draft",
                })
                drafts_created.append({
                    "channel": channel,
                    "touch_number": touch_num,
                    "draft_id": draft["id"],
                    "action": "created",
                })
        
        return {
            "status": "completed",
            "drafts_created": drafts_created,
            "email_suppressed": email_suppressed,
        }
    
    def _qa_task(self, contact_id: str) -> dict:
        """QA agent: check drafts for grounding, tone, compliance."""
        messages = models.get_messages_for_contact(contact_id)
        if not messages:
            return {"status": "completed", "passed": True, "checks": [], "note": "No messages to QA"}
        
        checks = []
        all_passed = True
        
        for msg in messages:
            msg_checks = []
            body = msg.get("body", "")
            
            # Check 1: No placeholder text
            placeholders = ["[DRAFT]", "[PENDING", "[TODO", "{company}", "{name}", "PLACEHOLDER"]
            has_placeholder = any(p in body for p in placeholders)
            msg_checks.append({"check": "no_placeholders", "passed": not has_placeholder})
            
            # Check 2: No em dashes
            has_em_dash = "\u2014" in body or "\u2013" in body
            msg_checks.append({"check": "no_em_dashes", "passed": not has_em_dash})
            
            # Check 3: Word count in bounds
            wc = len(body.split())
            touch = msg.get("touch_number", 1)
            if touch == 1:
                wc_ok = 70 <= wc <= 120
            elif touch in (3, 5):
                wc_ok = 40 <= wc <= 120
            elif touch == 6:
                wc_ok = 30 <= wc <= 50
            else:
                wc_ok = wc > 0
            msg_checks.append({"check": "word_count_ok", "passed": wc_ok, "word_count": wc})
            
            # Check 4: Has subject line
            has_subject = bool(msg.get("subject_line") and not msg["subject_line"].startswith("[DRAFT]"))
            msg_checks.append({"check": "has_subject", "passed": has_subject})
            
            # Check 5: Not fabricated (check for known proof points only)
            valid_proof_points = {"hansard", "medibuddy", "cred", "sanofi", "nagra", "spendflo", "fortune 100"}
            proof = (msg.get("proof_point_used") or "").lower()
            proof_ok = not proof or any(vp in proof for vp in valid_proof_points)
            msg_checks.append({"check": "valid_proof_point", "passed": proof_ok})
            
            passed = all(c["passed"] for c in msg_checks)
            if not passed:
                all_passed = False
            
            checks.append({
                "message_id": msg["id"],
                "touch_number": msg.get("touch_number"),
                "channel": msg.get("channel"),
                "passed": passed,
                "checks": msg_checks,
            })
        
        return {
            "status": "completed",
            "passed": all_passed,
            "total_messages": len(messages),
            "passed_count": sum(1 for c in checks if c["passed"]),
            "failed_count": sum(1 for c in checks if not c["passed"]),
            "checks": checks,
        }
    
    def _sequence_task(self, contact_id: str) -> dict:
        """Sequencer agent: propose follow-up timing and next steps."""
        contact = models.get_contact(contact_id)
        if not contact:
            return {"status": "error", "error": "Contact not found"}
        
        # Check if follow-ups already exist
        conn = models.get_db()
        existing = conn.execute("SELECT * FROM followups WHERE contact_id=? AND state='pending'",
                               (contact_id,)).fetchall()
        conn.close()
        
        if existing:
            return {
                "status": "completed",
                "action": "skipped",
                "reason": "Follow-ups already scheduled",
                "existing_count": len(existing),
            }
        
        # Create follow-up schedule based on SOP timing
        schedule = []
        channel_map = {
            1: ("linkedin", 0),    # Day 1: InMail
            2: ("call", 2),        # Day 3: Cold Call
            3: ("linkedin", 4),    # Day 5: InMail Follow-up
            4: ("call", 7),        # Day 8: Cold Call #2
            5: ("email", 9),       # Day 10: Email
            6: ("linkedin", 14),   # Day 15: Break-up
        }
        
        has_email = bool(contact.get("email"))
        
        for touch_num, (channel, days) in channel_map.items():
            if channel == "email" and not has_email:
                continue
            if channel == "call":
                continue  # Calls are manual, don't schedule as followups
            
            fu = models.schedule_followup(contact_id, touch_num, channel, days)
            schedule.append({
                "touch_number": touch_num,
                "channel": channel,
                "days_from_now": days,
                "followup_id": fu["id"],
            })
        
        return {
            "status": "completed",
            "followups_created": len(schedule),
            "schedule": schedule,
        }
    
    def cancel(self):
        """Cancel the swarm run."""
        self.cancelled = True
        if self.run_id:
            models.update_swarm_run(self.run_id, {"status": "cancelled"})
    
    def _finalize(self, status: str, results: dict):
        """Finalize the swarm run."""
        if self.run_id:
            models.update_swarm_run(self.run_id, {
                "status": status,
                "completed_at": datetime.utcnow().isoformat(),
            })
        self._emit("swarm_completed", {"run_id": self.run_id, "status": status})
        logger.info(f"Swarm run {self.run_id} finalized with status: {status}")


# ─── INSIGHTS AGENT ────────────────────────────────────────────

class InsightsAgent:
    """Produces daily and weekly performance reviews."""
    
    @staticmethod
    def daily_summary() -> dict:
        """Generate daily performance summary."""
        conn = models.get_db()
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        # Today's activity
        touches_today = conn.execute(
            "SELECT COUNT(*) FROM touchpoints WHERE sent_at >= ?", (today,)
        ).fetchone()[0]
        
        replies_today = conn.execute(
            "SELECT COUNT(*) FROM replies WHERE replied_at >= ?", (today,)
        ).fetchone()[0]
        
        meetings_today = conn.execute(
            "SELECT COUNT(*) FROM opportunities WHERE created_at >= ?", (today,)
        ).fetchone()[0]
        
        # Pending actions
        due_followups = conn.execute(
            "SELECT COUNT(*) FROM followups WHERE state='pending' AND due_date <= ?", (today,)
        ).fetchone()[0]
        
        pending_approvals = conn.execute(
            "SELECT COUNT(*) FROM message_drafts WHERE approval_status IN ('draft','pending')"
        ).fetchone()[0]
        
        # Active swarm runs
        active_swarms = conn.execute(
            "SELECT COUNT(*) FROM swarm_runs WHERE status='running'"
        ).fetchone()[0]
        
        # Email health
        email_health = models.get_email_health()
        
        conn.close()
        
        return {
            "date": today,
            "activity": {
                "touches_sent": touches_today,
                "replies_received": replies_today,
                "meetings_booked": meetings_today,
            },
            "pending": {
                "due_followups": due_followups,
                "pending_approvals": pending_approvals,
                "active_swarms": active_swarms,
            },
            "email_health": email_health,
            "recommendations": [],
        }
    
    @staticmethod
    def weekly_review() -> dict:
        """Generate weekly performance review with trends."""
        conn = models.get_db()
        
        # Last 7 days
        week_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()
        
        touches_week = conn.execute(
            "SELECT COUNT(*) FROM touchpoints WHERE sent_at >= ?", (week_ago,)
        ).fetchone()[0]
        
        replies_week = conn.execute(
            "SELECT COUNT(*) FROM replies WHERE replied_at >= ?", (week_ago,)
        ).fetchone()[0]
        
        meetings_week = conn.execute(
            "SELECT COUNT(*) FROM opportunities WHERE created_at >= ?", (week_ago,)
        ).fetchone()[0]
        
        # Reply rate
        reply_rate = round(replies_week / max(touches_week, 1) * 100, 1)
        
        # By channel
        channel_stats = conn.execute("""
            SELECT channel, COUNT(*) as cnt FROM touchpoints
            WHERE sent_at >= ? GROUP BY channel
        """, (week_ago,)).fetchall()
        
        conn.close()
        
        return {
            "period": f"Last 7 days (since {week_ago[:10]})",
            "summary": {
                "touches": touches_week,
                "replies": replies_week,
                "meetings": meetings_week,
                "reply_rate": reply_rate,
            },
            "by_channel": {r["channel"]: r["cnt"] for r in channel_stats},
        }
