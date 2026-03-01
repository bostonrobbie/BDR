"""
Memory Layer - Loader Module

Provides a clean API for agents to query the BDR second brain:
- Competitor battle cards (by tool name)
- Win/loss patterns (aggregated insights)
- Call notes (by contact or account)
- Market intel (industry trends, analyst coverage)
- Displacement playbooks (tool-specific outreach angles)

Usage:
    from src.memory.loader import MemoryLoader

    mem = MemoryLoader()
    card = mem.get_battle_card("selenium")
    angles = mem.get_displacement_angles("cypress")
    objection = mem.get_objection_response("playwright", "Our team knows Playwright")
"""

import json
import os
import re
from glob import glob
from typing import Optional


MEMORY_ROOT = os.path.join(os.path.dirname(__file__), "../../memory")


class MemoryLoader:
    """Read-only interface to the memory layer."""

    def __init__(self, memory_root: str = None):
        self.root = memory_root or MEMORY_ROOT
        self._index_cache = None
        self._card_cache = {}

    # ─── COMPETITOR INTELLIGENCE ─────────────────────────────────

    def _load_index(self) -> dict:
        """Load the competitor tool index."""
        if self._index_cache is not None:
            return self._index_cache
        path = os.path.join(self.root, "competitors", "_index.json")
        try:
            with open(path, "r") as f:
                self._index_cache = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._index_cache = {"tools": {}}
        return self._index_cache

    def resolve_tool_name(self, tool_name: str) -> Optional[str]:
        """Resolve a tool name or alias to the canonical key.

        Args:
            tool_name: Any tool name or alias (e.g., "webdriver", "tricentis", "qtp")

        Returns:
            Canonical tool key (e.g., "selenium", "tosca", "uft") or None.
        """
        index = self._load_index()
        name_lower = tool_name.lower().strip()

        # Direct key match
        if name_lower in index.get("tools", {}):
            return name_lower

        # Alias match
        for key, info in index.get("tools", {}).items():
            for alias in info.get("aliases", []):
                if alias.lower() == name_lower:
                    return key

        return None

    def get_battle_card(self, tool_name: str) -> Optional[dict]:
        """Get the full battle card for a competitor tool.

        Args:
            tool_name: Tool name or alias.

        Returns:
            Dict with sections: overview, strengths, weaknesses, displacement_proof_points,
            objections, talk_track, pricing. Returns None if no card found.
        """
        canonical = self.resolve_tool_name(tool_name)
        if not canonical:
            return None

        if canonical in self._card_cache:
            return self._card_cache[canonical]

        index = self._load_index()
        tool_info = index["tools"].get(canonical, {})
        filename = tool_info.get("file", f"{canonical}.md")
        path = os.path.join(self.root, "competitors", filename)

        try:
            with open(path, "r") as f:
                content = f.read()
        except FileNotFoundError:
            return None

        card = self._parse_battle_card(content, canonical, tool_info)
        self._card_cache[canonical] = card
        return card

    def _parse_battle_card(self, content: str, tool_key: str, tool_info: dict) -> dict:
        """Parse a markdown battle card into structured sections."""
        sections = {}
        current_section = None
        current_lines = []

        for line in content.split("\n"):
            if line.startswith("## "):
                if current_section:
                    sections[current_section] = "\n".join(current_lines).strip()
                current_section = line[3:].strip().lower().replace(" ", "_")
                current_lines = []
            elif current_section:
                current_lines.append(line)

        if current_section:
            sections[current_section] = "\n".join(current_lines).strip()

        return {
            "tool": tool_key,
            "category": tool_info.get("category", "unknown"),
            "threat_level": tool_info.get("threat_level", "unknown"),
            "prevalence": tool_info.get("prevalence", "unknown"),
            "sections": sections,
            "raw": content,
        }

    def get_displacement_angles(self, tool_name: str) -> list:
        """Get specific displacement angles for a competitor tool.

        Returns a list of dicts with: weakness, testsigma_angle, proof_point.
        These are the key arguments for why a prospect should switch.
        """
        card = self.get_battle_card(tool_name)
        if not card:
            return []

        weaknesses_text = card["sections"].get(
            "where_{}_{}_short_(our_angle)".format(
                tool_name.lower(), "falls"
            ), ""
        )

        # Try multiple section name patterns
        for key, text in card["sections"].items():
            if "falls_short" in key or "our_angle" in key:
                weaknesses_text = text
                break

        angles = []
        current_weakness = None
        current_angle = None

        for line in weaknesses_text.split("\n"):
            if line.startswith("### "):
                if current_weakness and current_angle:
                    angles.append({
                        "weakness": current_weakness,
                        "testsigma_angle": current_angle,
                    })
                current_weakness = line[4:].strip()
                current_angle = None
            elif "**Testsigma angle:**" in line:
                current_angle = line.split("**Testsigma angle:**")[-1].strip()

        if current_weakness and current_angle:
            angles.append({
                "weakness": current_weakness,
                "testsigma_angle": current_angle,
            })

        return angles

    def get_objection_response(self, tool_name: str, objection_text: str = "") -> Optional[dict]:
        """Get the best pre-loaded objection response for a tool.

        Args:
            tool_name: The competitor tool.
            objection_text: Optional text of the actual objection for matching.

        Returns:
            Dict with: objection, response, context. Or None.
        """
        card = self.get_battle_card(tool_name)
        if not card:
            return None

        objection_section = ""
        for key, text in card["sections"].items():
            if "objection" in key and "displac" in key:
                objection_section = text
                break

        if not objection_section:
            return None

        # Parse the table
        objections = []
        rows = [l for l in objection_section.split("\n") if l.strip().startswith("|") and "---" not in l]
        for row in rows[1:]:  # Skip header
            cells = [c.strip().strip('"') for c in row.split("|")[1:-1]]
            if len(cells) >= 2:
                objections.append({
                    "objection": cells[0].strip(),
                    "response": cells[1].strip(),
                })

        if not objections:
            return None

        # If objection_text provided, try to match
        if objection_text:
            text_lower = objection_text.lower()
            for obj in objections:
                # Simple keyword overlap scoring
                obj_words = set(obj["objection"].lower().split())
                text_words = set(text_lower.split())
                overlap = len(obj_words & text_words)
                if overlap >= 2:
                    return obj

        # Return the first (most common) objection
        return objections[0] if objections else None

    def get_talk_track(self, tool_name: str) -> Optional[str]:
        """Get the talk track guidance for a competitor tool."""
        card = self.get_battle_card(tool_name)
        if not card:
            return None

        for key, text in card["sections"].items():
            if "talk_track" in key:
                return text

        return None

    # ─── WIN/LOSS INTELLIGENCE ───────────────────────────────────

    def get_wins(self) -> list:
        """Get all win reports as parsed dicts."""
        return self._load_reports("wins")

    def get_losses(self) -> list:
        """Get all loss reports as parsed dicts."""
        return self._load_reports("losses")

    def _load_reports(self, report_type: str) -> list:
        """Load all reports of a given type from their directory."""
        pattern = os.path.join(self.root, report_type, "*.md")
        reports = []
        for path in sorted(glob(pattern)):
            filename = os.path.basename(path)
            if filename.startswith("_"):
                continue  # Skip templates
            with open(path, "r") as f:
                content = f.read()
            reports.append({
                "filename": filename,
                "path": path,
                "content": content,
                "tags": self._extract_tags(content),
            })
        return reports

    def _extract_tags(self, content: str) -> dict:
        """Extract tag values from a report's Tags section."""
        tags = {}
        in_tags = False
        for line in content.split("\n"):
            if line.strip() == "## Tags":
                in_tags = True
                continue
            if in_tags:
                if line.startswith("## "):
                    break
                match = re.match(r"^- (\w[\w\s]*?):\s*(.+)", line)
                if match:
                    key = match.group(1).strip().lower().replace(" ", "_")
                    tags[key] = match.group(2).strip()
        return tags

    def get_win_patterns(self) -> dict:
        """Analyze wins to identify patterns.

        Returns:
            Dict with: top_pains, top_verticals, top_proof_points, top_objections_overcome.
        """
        wins = self.get_wins()
        if not wins:
            return {"top_pains": [], "top_verticals": [], "top_proof_points": [],
                    "note": "No win reports yet. Add reports to memory/wins/ to enable pattern detection."}

        from collections import Counter
        pains = Counter()
        verticals = Counter()
        competitors = Counter()

        for w in wins:
            t = w.get("tags", {})
            if t.get("pain"):
                pains[t["pain"]] += 1
            if t.get("vertical"):
                verticals[t["vertical"]] += 1
            if t.get("competitor_displaced"):
                competitors[t["competitor_displaced"]] += 1

        return {
            "total_wins": len(wins),
            "top_pains": pains.most_common(5),
            "top_verticals": verticals.most_common(5),
            "top_competitors_displaced": competitors.most_common(5),
        }

    # ─── CALL NOTES ──────────────────────────────────────────────

    def get_call_notes(self, contact_name: str = None, account_name: str = None) -> list:
        """Get call notes, optionally filtered by contact or account name.

        Args:
            contact_name: Filter by prospect name (partial match).
            account_name: Filter by company name (partial match).

        Returns:
            List of call note dicts with filename, content, tags.
        """
        pattern = os.path.join(self.root, "call-notes", "*.md")
        notes = []
        for path in sorted(glob(pattern), reverse=True):  # Most recent first
            filename = os.path.basename(path)
            if filename.startswith("_"):
                continue

            # Quick filename-based filtering before reading content
            if contact_name:
                name_parts = contact_name.lower().split()
                fn_lower = filename.lower()
                if not any(part in fn_lower for part in name_parts):
                    continue

            with open(path, "r") as f:
                content = f.read()

            if account_name and account_name.lower() not in content.lower():
                continue

            notes.append({
                "filename": filename,
                "path": path,
                "content": content,
                "tags": self._extract_tags(content),
            })
        return notes

    # ─── MARKET INTELLIGENCE ─────────────────────────────────────

    def get_market_intel(self) -> dict:
        """Get all market intelligence files."""
        intel = {}
        pattern = os.path.join(self.root, "market-intel", "*.md")
        for path in sorted(glob(pattern)):
            filename = os.path.basename(path)
            with open(path, "r") as f:
                intel[filename] = f.read()
        return intel

    def get_competitor_moves(self) -> str:
        """Get just the competitor moves section from market intel."""
        intel = self.get_market_intel()
        trends = intel.get("industry-trends.md", "")
        in_section = False
        lines = []
        for line in trends.split("\n"):
            if "## Competitor Moves" in line:
                in_section = True
                continue
            if in_section:
                if line.startswith("## "):
                    break
                lines.append(line)
        return "\n".join(lines).strip()

    # ─── SALES PLAYBOOK ─────────────────────────────────────────

    def get_playbook(self) -> Optional[str]:
        """Get the sales playbook quick reference."""
        path = os.path.join(self.root, "context", "sales-playbook.md")
        try:
            with open(path, "r") as f:
                return f.read()
        except FileNotFoundError:
            return None

    # ─── COMPOSITE QUERIES ───────────────────────────────────────

    def get_prospect_context(self, known_tools: list = None,
                              vertical: str = None,
                              account_name: str = None) -> dict:
        """Get all relevant memory context for a prospect.

        This is the main integration point for message_writer and researcher.
        Pulls battle cards, displacement angles, objection responses, relevant
        win/loss data, and call notes into a single context object.

        Args:
            known_tools: List of tools the prospect uses.
            vertical: The prospect's industry vertical.
            account_name: Company name for call note lookup.

        Returns:
            Composite context dict with all relevant memory data.
        """
        context = {
            "battle_cards": [],
            "displacement_angles": [],
            "objection_responses": [],
            "talk_tracks": [],
            "prior_call_notes": [],
            "vertical_trends": None,
        }

        # Load battle cards for detected tools
        for tool in (known_tools or []):
            card = self.get_battle_card(tool)
            if card:
                context["battle_cards"].append({
                    "tool": card["tool"],
                    "threat_level": card["threat_level"],
                    "category": card["category"],
                })

                angles = self.get_displacement_angles(tool)
                if angles:
                    context["displacement_angles"].extend([
                        {**a, "tool": card["tool"]} for a in angles
                    ])

                obj = self.get_objection_response(tool)
                if obj:
                    context["objection_responses"].append({
                        **obj, "tool": card["tool"]
                    })

                track = self.get_talk_track(tool)
                if track:
                    context["talk_tracks"].append({
                        "tool": card["tool"],
                        "guidance": track,
                    })

        # Load prior call notes for the account
        if account_name:
            notes = self.get_call_notes(account_name=account_name)
            context["prior_call_notes"] = [
                {"filename": n["filename"], "tags": n["tags"]}
                for n in notes[:5]  # Limit to 5 most recent
            ]

        # Load vertical-specific trends
        if vertical:
            intel = self.get_market_intel()
            trends = intel.get("industry-trends.md", "")
            vertical_lower = vertical.lower()
            for line in trends.split("\n"):
                if vertical_lower in line.lower():
                    if not context["vertical_trends"]:
                        context["vertical_trends"] = []
                    context["vertical_trends"].append(line.strip())

        return context


# Module-level convenience instance
_default_loader = None


def get_memory() -> MemoryLoader:
    """Get the default MemoryLoader singleton."""
    global _default_loader
    if _default_loader is None:
        _default_loader = MemoryLoader()
    return _default_loader
