"""
Outreach Command Center - Batch Builder (Pipeline Orchestrator)
Coordinates the full prospect-to-deliverable pipeline:
Pre-Brief → Extract → Research → Score → A/B Assign → Messages → QC → HTML

This module defines the pipeline steps and data contracts.
Actual execution happens in Cowork sessions where Claude calls each step.
"""

import json
import os
import sys
from datetime import datetime
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models


# ─── BATCH CONFIG ─────────────────────────────────────────────

DEFAULT_CONFIG = {
    "target_count": 25,
    "ab_variable": "pain_hook",
    "ab_groups": {
        "A": "Flaky/brittle tests (maintenance angle)",
        "B": "Release velocity/speed angle"
    },
    "mix_ratio": {
        "qa_leaders": {"min": 12, "max": 15},
        "vp_eng": {"min": 8, "max": 10},
        "buyer_intent": {"min": 2, "max": 3}
    },
    "max_per_vertical": 8,
    "max_per_company": 2,
}


# ─── PIPELINE PHASES ──────────────────────────────────────────

class BatchPipeline:
    """Orchestrates the batch building pipeline."""

    def __init__(self, batch_number: int, config: dict = None):
        self.batch_number = batch_number
        self.config = {**DEFAULT_CONFIG, **(config or {})}
        self.batch_id = None
        self.run_id = None
        self.contacts = []
        self.messages = []
        self.start_time = None
        self.phase_log = []

    def initialize(self) -> dict:
        """Phase 0: Create batch record and start agent run logging."""
        self.start_time = datetime.utcnow()

        # Create batch in DB
        batch = models.create_batch({
            "batch_number": self.batch_number,
            "prospect_count": self.config["target_count"],
            "ab_variable": self.config["ab_variable"],
            "ab_description": json.dumps(self.config.get("ab_groups", {})),
            "mix_ratio": self.config.get("mix_ratio", {}),
            "status": "building",
        })
        self.batch_id = batch["id"]

        # Log the orchestrator run
        run = models.start_agent_run(
            run_type="batch_build",
            agent_name="BatchBuilder",
            batch_id=self.batch_id,
            inputs={"batch_number": self.batch_number, "config": self.config},
        )
        self.run_id = run["id"]

        self._log_phase("initialize", "Batch created", {"batch_id": self.batch_id})
        return batch

    def phase_pre_brief(self) -> Optional[dict]:
        """Phase 1: Generate pre-brief from previous batch data (skip if batch 1)."""
        if self.batch_number <= 1:
            self._log_phase("pre_brief", "Skipped (first batch)")
            return None

        from src.agents.pre_brief import generate_pre_brief
        brief = generate_pre_brief()
        self._log_phase("pre_brief", "Generated", brief)
        return brief

    def phase_extract(self, prospects: list) -> list:
        """Phase 2: Accept extracted prospects from Sales Nav.

        prospects: list of dicts with keys:
            first_name, last_name, title, company, linkedin_url,
            headline, persona_type, location

        Returns list of created contact IDs.
        """
        contact_ids = []
        for p in prospects:
            # Create or find account
            account = self._ensure_account(p)

            # Create contact
            contact = models.create_contact({
                "account_id": account["id"],
                "first_name": p["first_name"],
                "last_name": p["last_name"],
                "title": p.get("title", ""),
                "persona_type": p.get("persona_type", ""),
                "seniority_level": p.get("seniority_level", ""),
                "linkedin_url": p.get("linkedin_url", ""),
                "location": p.get("location", "US"),
                "email": p.get("email"),
                "tenure_months": p.get("tenure_months"),
                "recently_hired": p.get("recently_hired", 0),
                "stage": "new",
                "source": "sales_nav",
            })
            contact_ids.append(contact["id"])

            # Link to batch
            self._link_contact_to_batch(contact["id"])

        self.contacts = contact_ids
        self._log_phase("extract", f"Stored {len(contact_ids)} prospects", {
            "count": len(contact_ids)
        })
        return contact_ids

    def phase_research(self, research_results: dict) -> None:
        """Phase 3: Accept research results and store them.

        research_results: dict mapping contact_id -> {
            person_research: {...},
            company_research: {...}
        }
        """
        for contact_id, research in research_results.items():
            # Save person research
            person = research.get("person_research", {})
            if person:
                models.save_research({
                    "contact_id": contact_id,
                    "entity_type": "person",
                    "headline": person.get("headline", ""),
                    "summary": person.get("about", ""),
                    "career_history": person.get("career_history", []),
                    "responsibilities": person.get("current_role_description", ""),
                    "sources": [person.get("source", "linkedin")],
                })

            # Save company research
            company = research.get("company_research", {})
            if company:
                contact = models.get_contact(contact_id)
                if contact and contact.get("account_id"):
                    models.save_research({
                        "account_id": contact["account_id"],
                        "entity_type": "company",
                        "summary": company.get("description", ""),
                        "tech_stack_signals": company.get("tech_stack", []),
                        "company_products": json.dumps(company.get("products", [])),
                        "company_news": company.get("recent_news", ""),
                        "hiring_signals": company.get("hiring_signals", ""),
                        "sources": company.get("sources", []),
                    })

                    # Update account with research findings
                    company = research["company_research"]
                    update_data = {}
                    if company.get("industry"):
                        update_data["industry"] = company["industry"]
                    if company.get("employee_count"):
                        update_data["employee_count"] = company["employee_count"]
                    if company.get("employee_band"):
                        update_data["employee_band"] = company["employee_band"]
                    if company.get("known_tools"):
                        update_data["known_tools"] = json.dumps(company["known_tools"])
                    if company.get("buyer_intent"):
                        update_data["buyer_intent"] = 1
                    if update_data:
                        models.update_account(contact["account_id"], update_data)

            # Update contact with person research findings
            person = research.get("person_research", {})
            contact_update = {}
            if person.get("tenure_months"):
                contact_update["tenure_months"] = person["tenure_months"]
            if person.get("recently_hired"):
                contact_update["recently_hired"] = 1
            if person.get("previous_company"):
                contact_update["previous_company"] = person["previous_company"]
            if person.get("previous_title"):
                contact_update["previous_title"] = person["previous_title"]
            if contact_update:
                models.update_contact(contact_id, contact_update)

        self._log_phase("research", f"Stored research for {len(research_results)} prospects")

    def phase_score(self) -> list:
        """Phase 4: Score all contacts (ICP + Priority)."""
        from src.agents.scorer import batch_score
        results = batch_score(self.contacts)
        self._log_phase("score", f"Scored {len(results)} contacts")
        return results

    def phase_ab_assign(self) -> dict:
        """Phase 5: Assign A/B groups."""
        from src.agents.ab_assigner import assign_ab_groups
        assignments = assign_ab_groups(
            self.contacts,
            self.config["ab_variable"],
            self.config["ab_groups"],
            self.batch_id
        )
        self._log_phase("ab_assign", f"Assigned {len(assignments)} to groups")
        return assignments

    def phase_messages(self, generated_messages: list) -> list:
        """Phase 6: Accept generated messages and store them.

        generated_messages: list of dicts, each with keys matching
        create_message_draft() expectations.
        """
        stored = []
        for msg in generated_messages:
            msg["batch_id"] = self.batch_id
            msg["agent_run_id"] = self.run_id
            result = models.create_message_draft(msg)
            stored.append(result)
        self.messages = stored
        self._log_phase("messages", f"Stored {len(stored)} messages")
        return stored

    def phase_qc(self) -> dict:
        """Phase 7: Run quality gate on all messages."""
        from src.agents.quality_gate import qc_and_save
        results = {"passed": 0, "failed": 0, "flags": []}
        for msg in self.messages:
            qc = qc_and_save(msg["id"])
            if qc.get("passed"):
                results["passed"] += 1
            else:
                results["failed"] += 1
                results["flags"].append({
                    "message_id": msg["id"],
                    "contact_id": msg["contact_id"],
                    "issues": qc.get("flags", [])
                })
        self._log_phase("qc", f"QC: {results['passed']} passed, {results['failed']} failed")
        return results

    def phase_generate_html(self) -> str:
        """Phase 8: Generate HTML deliverable.

        Returns path to generated file.
        """
        from src.agents.deliverable_generator import generate_batch_html
        output_path = generate_batch_html(self.batch_id, self.batch_number)
        self._log_phase("generate_html", f"HTML saved to {output_path}")
        return output_path

    def finalize(self) -> dict:
        """Phase 9: Mark batch as complete, finalize agent run."""
        conn = models.get_db()
        conn.execute("UPDATE batches SET status='complete' WHERE id=?", (self.batch_id,))
        conn.commit()
        conn.close()

        duration_ms = int((datetime.utcnow() - self.start_time).total_seconds() * 1000)
        models.complete_agent_run(
            run_id=self.run_id,
            outputs={
                "contacts": len(self.contacts),
                "messages": len(self.messages),
                "phases": self.phase_log,
            },
            tokens=0,
        )

        self._log_phase("finalize", "Batch complete", {
            "duration_ms": duration_ms,
            "contacts": len(self.contacts),
            "messages": len(self.messages)
        })

        return {
            "batch_id": self.batch_id,
            "batch_number": self.batch_number,
            "contacts": len(self.contacts),
            "messages": len(self.messages),
            "phases": self.phase_log,
            "duration_ms": duration_ms,
        }

    # ─── HELPERS ──────────────────────────────────────────────

    def _ensure_account(self, prospect: dict) -> dict:
        """Find or create account for a prospect's company."""
        company = prospect.get("company", "")
        if not company:
            return models.create_account({"name": "Unknown"})

        # Check if account already exists by name
        conn = models.get_db()
        row = conn.execute(
            "SELECT * FROM accounts WHERE LOWER(name)=?",
            (company.lower(),)
        ).fetchone()
        conn.close()

        if row:
            return dict(row)

        return models.create_account({
            "name": company,
            "industry": prospect.get("vertical", ""),
        })

    def _link_contact_to_batch(self, contact_id: str):
        """Add contact to batch_prospects join table."""
        conn = models.get_db()
        try:
            conn.execute(
                "INSERT INTO batch_prospects (batch_id, contact_id) VALUES (?,?)",
                (self.batch_id, contact_id)
            )
            conn.commit()
        except Exception:
            pass  # Duplicate, ignore
        finally:
            conn.close()

    def _log_phase(self, phase: str, message: str, data: dict = None):
        """Log a pipeline phase completion."""
        entry = {
            "phase": phase,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        }
        if data:
            entry["data"] = data
        self.phase_log.append(entry)


# ─── CONVENIENCE FUNCTION ─────────────────────────────────────

def get_batch_status(batch_id: str) -> dict:
    """Get current status of a batch and its pipeline progress."""
    conn = models.get_db()
    batch = conn.execute("SELECT * FROM batches WHERE id=?", (batch_id,)).fetchone()
    if not batch:
        conn.close()
        return {"error": "Batch not found"}

    contacts = conn.execute(
        "SELECT COUNT(*) as cnt FROM batch_prospects WHERE batch_id=?",
        (batch_id,)
    ).fetchone()

    messages = conn.execute(
        "SELECT COUNT(*) as cnt, SUM(qc_passed) as qc_ok FROM message_drafts WHERE batch_id=?",
        (batch_id,)
    ).fetchone()

    conn.close()

    return {
        "batch": dict(batch),
        "contacts": contacts["cnt"],
        "messages": messages["cnt"],
        "messages_qc_passed": messages["qc_ok"] or 0,
    }
