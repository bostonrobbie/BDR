"""
Outreach Command Center - Deliverable Generator
Generates self-contained HTML batch files with all prospect data, messages,
call snippets, objections, research, status tracking, and localStorage persistence.

Output: /mnt/Work/prospect-outreach-[batch#]-[date].html
"""

import json
import os
import sys
from datetime import datetime
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.db import models


# ─── MAIN ENTRY POINT ───────────────────────────────────────

def generate_batch_html(batch_id: str, batch_number: int, output_dir: str = None) -> str:
    """Generate the complete HTML deliverable for a batch.

    Queries all data from DB: contacts, messages, research, signals, experiments.
    Returns the output file path.
    """
    if not output_dir:
        output_dir = os.environ.get(
            "OCC_OUTPUT_DIR",
            os.path.join(os.path.dirname(__file__), "../../output")
        )
    os.makedirs(output_dir, exist_ok=True)

    # Gather all data
    data = _gather_batch_data(batch_id)
    if not data:
        return ""

    # Build HTML
    html = _render_full_html(data, batch_number)

    # Write file
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"prospect-outreach-{batch_number}-{date_str}.html"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filepath


# ─── DATA GATHERING ──────────────────────────────────────────

def _gather_batch_data(batch_id: str) -> Optional[dict]:
    """Pull all batch data from DB into a single dict."""
    conn = models.get_db()

    # Batch info
    batch = conn.execute("SELECT * FROM batches WHERE id=?", (batch_id,)).fetchone()
    if not batch:
        conn.close()
        return None
    batch = dict(batch)

    # Contacts in this batch
    rows = conn.execute("""
        SELECT c.*, a.name as company_name, a.industry, a.employee_count,
               a.employee_band, a.known_tools, a.buyer_intent, a.domain,
               bp.ab_group, bp.position_in_batch
        FROM batch_prospects bp
        JOIN contacts c ON bp.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        WHERE bp.batch_id = ?
        ORDER BY c.priority_score DESC
    """, (batch_id,)).fetchall()
    contacts = [dict(r) for r in rows]

    # Messages for all contacts in batch
    msg_rows = conn.execute("""
        SELECT * FROM message_drafts WHERE batch_id = ?
        ORDER BY contact_id, touch_number ASC
    """, (batch_id,)).fetchall()
    messages_by_contact = {}
    for m in msg_rows:
        m = dict(m)
        cid = m["contact_id"]
        if cid not in messages_by_contact:
            messages_by_contact[cid] = []
        messages_by_contact[cid].append(m)

    # Research snapshots for contacts
    research_by_contact = {}
    for c in contacts:
        person_rs = conn.execute("""
            SELECT * FROM research_snapshots
            WHERE contact_id=? AND entity_type='person'
            ORDER BY created_at DESC LIMIT 1
        """, (c["id"],)).fetchone()
        company_rs = conn.execute("""
            SELECT * FROM research_snapshots
            WHERE account_id=? AND entity_type='company'
            ORDER BY created_at DESC LIMIT 1
        """, (c.get("account_id", ""),)).fetchone()

        person_data = {}
        if person_rs:
            pr = dict(person_rs)
            person_data = {
                "headline": pr.get("headline", ""),
                "about": pr.get("summary", ""),
                "current_role_description": pr.get("responsibilities", ""),
                "career_history": json.loads(pr["career_history"]) if pr.get("career_history") else [],
                "recently_hired": False,
                "tenure_months": None,
            }

        company_data = {}
        if company_rs:
            cr = dict(company_rs)
            company_data = {
                "description": cr.get("summary", ""),
                "known_tools": json.loads(cr["tech_stack_signals"]) if cr.get("tech_stack_signals") else [],
                "recent_news": cr.get("company_news", ""),
                "hiring_signals": cr.get("hiring_signals", ""),
                "vertical": c.get("industry", ""),
                "employee_band": c.get("employee_band", ""),
            }

        research_by_contact[c["id"]] = {
            "person": person_data,
            "company": company_data,
        }

    # Signals
    signals_by_contact = {}
    for c in contacts:
        sig_rows = conn.execute("""
            SELECT * FROM signals
            WHERE contact_id=? OR account_id=?
            ORDER BY detected_at DESC
        """, (c["id"], c.get("account_id", ""))).fetchall()
        signals_by_contact[c["id"]] = [dict(s) for s in sig_rows]

    # Experiment info
    experiment = None
    exp_rows = conn.execute("""
        SELECT * FROM experiments
        WHERE batches_included LIKE ?
        ORDER BY created_at DESC LIMIT 1
    """, (f"%{batch_id}%",)).fetchall()
    if exp_rows:
        experiment = dict(exp_rows[0])

    # Pre-brief (from agent_runs if available)
    pre_brief = None
    pb_row = conn.execute("""
        SELECT outputs FROM agent_runs
        WHERE agent_name='PreBrief' AND run_type='pre_brief'
        ORDER BY started_at DESC LIMIT 1
    """).fetchone()
    if pb_row and pb_row["outputs"]:
        try:
            pre_brief = json.loads(pb_row["outputs"])
        except (json.JSONDecodeError, TypeError):
            pass

    conn.close()

    return {
        "batch": batch,
        "contacts": contacts,
        "messages": messages_by_contact,
        "research": research_by_contact,
        "signals": signals_by_contact,
        "experiment": experiment,
        "pre_brief": pre_brief,
    }


# ─── HTML RENDERING ──────────────────────────────────────────

def _render_full_html(data: dict, batch_number: int) -> str:
    """Render the complete HTML document."""
    batch = data["batch"]
    contacts = data["contacts"]
    experiment = data["experiment"]
    pre_brief = data["pre_brief"]

    # Compute stats
    stats = _compute_batch_stats(contacts)

    date_str = datetime.utcnow().strftime("%b %d, %Y")
    ab_var = batch.get("ab_variable", "")
    ab_desc = ""
    if experiment:
        ab_desc = f"{experiment.get('variable', ab_var)}: A = {experiment.get('group_a_desc', '')}, B = {experiment.get('group_b_desc', '')}"

    parts = []
    parts.append(_render_head(batch_number, date_str))
    parts.append('<body>\n<div class="container">\n')

    # Header
    parts.append(f'<h1>Testsigma Prospect Outreach - Batch {batch_number}</h1>\n')
    parts.append(f'<p class="subtitle">{stats["total"]} Prospects with Research-Backed Personalized Sequences - {date_str}</p>\n')

    # Pre-brief
    if pre_brief:
        parts.append(_render_pre_brief(pre_brief))

    # Stats bar
    parts.append(_render_stats_bar(stats))

    # A/B test info
    if ab_desc:
        parts.append(f'<div class="ab-info"><strong>A/B Test:</strong> {_esc(ab_desc)}</div>\n')

    # Filters
    parts.append(_render_filters())

    # Tracker table
    parts.append(_render_tracker_table(contacts, data))

    # Prospect cards
    parts.append('<h2 class="section-title">Prospect Detail Cards</h2>\n')
    for i, c in enumerate(contacts):
        cid = c["id"]
        msgs = data["messages"].get(cid, [])
        research = data["research"].get(cid, {})
        signals = data["signals"].get(cid, [])
        parts.append(_render_prospect_card(i + 1, c, msgs, research, signals))

    parts.append('</div>\n')  # close container
    parts.append(_render_scripts(contacts))
    parts.append('</body>\n</html>')

    return "\n".join(parts)


def _compute_batch_stats(contacts: list) -> dict:
    """Compute summary stats for the batch."""
    qa_count = sum(1 for c in contacts if c.get("persona_type") == "QA")
    vp_count = sum(1 for c in contacts if c.get("persona_type") == "VP Eng")
    inf_count = sum(1 for c in contacts if c.get("persona_type") == "Influencer")
    intent_count = sum(1 for c in contacts if c.get("buyer_intent"))

    hot = sum(1 for c in contacts if (c.get("priority_score") or 0) >= 5)
    warm = sum(1 for c in contacts if (c.get("priority_score") or 0) == 4)

    verticals = {}
    for c in contacts:
        v = c.get("industry") or "Other"
        verticals[v] = verticals.get(v, 0) + 1

    return {
        "total": len(contacts),
        "qa_leaders": qa_count,
        "vp_eng": vp_count,
        "influencers": inf_count,
        "buyer_intent": intent_count,
        "hot": hot,
        "warm": warm,
        "verticals": verticals,
    }


# ─── HTML SECTIONS ───────────────────────────────────────────

def _render_head(batch_number: int, date_str: str) -> str:
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Testsigma Prospect Outreach - Batch {batch_number} ({date_str})</title>
<style>
{_get_css()}
</style>
</head>'''


def _render_pre_brief(brief: dict) -> str:
    """Render the 5-line pre-brief at the top."""
    lines = brief if isinstance(brief, list) else brief.get("insights", [])
    if not lines:
        return ""

    html = '<div class="pre-brief">\n'
    html += '<h3>Pre-Brief: What\'s Working</h3>\n<ul>\n'
    for line in lines[:5]:
        if isinstance(line, dict):
            text = line.get("text", line.get("insight", str(line)))
        else:
            text = str(line)
        html += f'  <li>{_esc(text)}</li>\n'
    html += '</ul>\n</div>\n'
    return html


def _render_stats_bar(stats: dict) -> str:
    boxes = [
        (stats["total"], "Prospects"),
        (stats["qa_leaders"], "QA Leaders"),
        (stats["vp_eng"], "VP Eng"),
        (stats["buyer_intent"], "Buyer Intent"),
        (stats["hot"], "Hot (5)"),
        (stats["warm"], "Warm (4)"),
    ]
    html = '<div class="stats">\n'
    for num, label in boxes:
        html += f'  <div class="stat-box"><div class="stat-num">{num}</div><div class="stat-label">{label}</div></div>\n'
    html += '</div>\n'
    return html


def _render_filters() -> str:
    return '''<div class="filter-bar">
  <label>Priority: <select id="filterPriority" onchange="applyFilters()">
    <option value="all">All</option>
    <option value="5">Hot (5)</option>
    <option value="4">Warm (4)</option>
    <option value="45">Hot + Warm</option>
  </select></label>
  <label>Persona: <select id="filterPersona" onchange="applyFilters()">
    <option value="all">All</option>
    <option value="QA">QA Leaders</option>
    <option value="VP Eng">VP Engineering</option>
    <option value="Influencer">Influencer</option>
  </select></label>
  <label>Status: <select id="filterStatus" onchange="applyFilters()">
    <option value="all">All</option>
    <option value="Not Started">Not Started</option>
    <option value="Touch 1 Sent">Touch 1 Sent</option>
    <option value="Replied">Replied</option>
    <option value="Meeting Booked">Meeting Booked</option>
  </select></label>
</div>
'''


def _render_tracker_table(contacts: list, data: dict) -> str:
    html = '<h2 class="section-title">Prospect Tracker</h2>\n'
    html += '<div class="table-wrap"><table>\n'
    html += '<thead><tr>'
    html += '<th>Pri</th><th>#</th><th>Name</th><th>Title</th><th>Company</th>'
    html += '<th>Tags</th><th>A/B</th><th>P.Score</th>'
    html += '<th>Status</th><th>Reply Tag</th><th>LinkedIn</th>'
    html += '</tr></thead>\n<tbody>\n'

    for i, c in enumerate(contacts):
        cid = c["id"]
        priority = c.get("priority_score") or 0
        persona = c.get("persona_type", "")
        vertical = c.get("industry", "")
        ab_group = c.get("ab_group", "")
        icp = c.get("priority_score") or 0
        buyer = c.get("buyer_intent", 0)
        li_url = c.get("linkedin_url", "")

        # Priority badge class
        pri_cls = "pri-hot" if priority >= 5 else "pri-warm" if priority == 4 else "pri-std" if priority == 3 else "pri-low"

        # Tags
        tags = _render_tags(persona, vertical, buyer)

        # Messages for personalization score
        msgs = data["messages"].get(cid, [])
        p_score = ""
        if msgs:
            ps = msgs[0].get("personalization_score")
            if ps:
                p_score = f'<span class="p-score p-score-{ps}">{ps}</span>'

        # LinkedIn link
        li_link = f'<a href="{_attr(li_url)}" target="_blank">Open</a>' if li_url else "-"

        html += f'<tr class="prospect-row" data-id="{_attr(cid)}" data-priority="{priority}" data-persona="{_attr(persona)}">\n'
        html += f'  <td><span class="pri-badge {pri_cls}">{priority}</span></td>\n'
        html += f'  <td>{i+1}</td>\n'
        html += f'  <td class="name-cell"><a href="#card-{_attr(cid)}" onclick="scrollToCard(\'{_attr(cid)}\')">{_esc(c.get("first_name",""))} {_esc(c.get("last_name",""))}</a></td>\n'
        html += f'  <td>{_esc(c.get("title",""))}</td>\n'
        html += f'  <td>{_esc(c.get("company_name",""))}</td>\n'
        html += f'  <td>{tags}</td>\n'
        html += f'  <td class="ab-cell">{_esc(ab_group)}</td>\n'
        html += f'  <td>{p_score}</td>\n'
        html += f'  <td>{_render_status_dropdown(cid)}</td>\n'
        html += f'  <td>{_render_reply_tag_dropdown(cid)}</td>\n'
        html += f'  <td class="url-cell">{li_link}</td>\n'
        html += '</tr>\n'

    html += '</tbody></table></div>\n'
    return html


def _render_tags(persona: str, vertical: str, buyer_intent: int) -> str:
    tags = ""
    if persona == "QA":
        tags += '<span class="badge badge-qa">QA</span>'
    elif persona == "VP Eng":
        tags += '<span class="badge badge-vp">VP Eng</span>'
    elif persona == "Influencer":
        tags += '<span class="badge badge-inf">Influencer</span>'

    vert_class = {
        "FinTech": "badge-fin", "FinServ": "badge-fin",
        "Healthcare": "badge-health", "SaaS": "badge-tech",
        "E-Commerce": "badge-ecom", "Insurance": "badge-fin",
        "InsurTech": "badge-fin", "Tech": "badge-tech",
        "Telecom": "badge-tel", "Pharma": "badge-health",
        "Retail": "badge-ecom",
    }.get(vertical, "badge-other")
    if vertical:
        tags += f'<span class="badge {vert_class}">{_esc(vertical)}</span>'

    if buyer_intent:
        tags += '<span class="badge badge-bi">Buyer Intent</span>'

    return tags


def _render_status_dropdown(contact_id: str) -> str:
    statuses = [
        "Not Started", "Touch 1 Sent", "Call 1 Made", "Touch 3 Sent",
        "Call 2 Made", "Touch 5 Sent", "Touch 6 Sent", "Replied",
        "Meeting Booked", "Not Interested", "Bounced", "Dormant", "Re-Engaged"
    ]
    cid = _attr(contact_id)
    html = f'<select class="status-dd" data-cid="{cid}" onchange="saveStatus(this)">\n'
    for s in statuses:
        html += f'  <option value="{_attr(s)}">{_esc(s)}</option>\n'
    html += '</select>'
    return html


def _render_reply_tag_dropdown(contact_id: str) -> str:
    tags = [
        "", "Opener", "Pain hook", "Proof point", "Timing",
        "Referral", "Not interested", "Unknown"
    ]
    cid = _attr(contact_id)
    html = f'<select class="reply-dd" data-cid="{cid}" onchange="saveReplyTag(this)">\n'
    for t in tags:
        label = t if t else "- Reply Tag -"
        html += f'  <option value="{_attr(t)}">{_esc(label)}</option>\n'
    html += '</select>'
    return html


def _render_prospect_card(idx: int, contact: dict, messages: list,
                          research: dict, signals: list) -> str:
    """Render a full expandable prospect detail card."""
    cid = contact["id"]
    name = f'{contact.get("first_name","")} {contact.get("last_name","")}'
    title = contact.get("title", "")
    company = contact.get("company_name", "")
    priority = contact.get("priority_score") or 0
    persona = contact.get("persona_type", "")
    ab_group = contact.get("ab_group", "")

    html = f'<div class="card" id="card-{_attr(cid)}">\n'
    html += f'<div class="card-header" onclick="toggleCard(\'{_attr(cid)}\')">\n'
    html += f'  <h3><span class="pri-badge pri-{"hot" if priority >= 5 else "warm" if priority == 4 else "std"}">{priority}</span> '
    html += f'{idx}. {_esc(name)}</h3>\n'
    html += f'  <p class="card-meta">{_esc(title)} &bull; {_esc(company)}'
    if ab_group:
        html += f' &bull; Group {_esc(ab_group)}'
    if persona:
        html += f' &bull; {_esc(persona)}'
    html += '</p>\n'
    html += '</div>\n'

    html += f'<div class="card-body" id="body-{_attr(cid)}" style="display:none;">\n'

    # Research section
    person_r = research.get("person", {})
    company_r = research.get("company", {})
    html += _render_research_section(person_r, company_r, signals)

    # Messages - all touches
    touch_types = {
        1: ("Touch 1 - InMail", "inmail"),
        2: ("Touch 2 - Call Snippet", "call"),
        3: ("Touch 3 - Follow-up InMail", "inmail"),
        4: ("Touch 4 - Call Snippet", "call"),
        5: ("Touch 5 - Email", "email"),
        6: ("Touch 6 - Break-up InMail", "inmail"),
    }

    for msg in messages:
        touch_num = msg.get("touch_number", 0)
        touch_label, touch_type = touch_types.get(touch_num, (f"Touch {touch_num}", "inmail"))
        msg_id = msg.get("id", f"msg-{cid}-{touch_num}")

        if touch_type == "call":
            html += _render_call_snippet(msg_id, touch_label, msg)
        else:
            html += _render_message_block(msg_id, touch_label, msg)

    # Objection mapping
    objection = None
    for msg in messages:
        if msg.get("predicted_objection"):
            objection = {
                "objection": msg.get("predicted_objection", ""),
                "response": msg.get("objection_response", ""),
            }
            break
    if objection:
        html += _render_objection(objection)

    # Meeting prep card (hidden by default, shown when status = Meeting Booked)
    html += _render_prep_card(contact, person_r, company_r, signals, messages)

    html += '</div>\n</div>\n'
    return html


def _render_research_section(person: dict, company: dict, signals: list) -> str:
    html = '<div class="research-section">\n'
    html += '<h4>Research</h4>\n'

    if person:
        html += '<div class="research-block">\n<strong>Profile:</strong> '
        parts = []
        if person.get("headline"):
            parts.append(person["headline"])
        if person.get("about"):
            parts.append(person["about"][:200])
        if person.get("current_role_description"):
            parts.append(person["current_role_description"][:200])
        if person.get("tenure_months"):
            parts.append(f"Tenure: {person['tenure_months']} months")
        if person.get("recently_hired"):
            parts.append("Recently hired (<6 months)")
        html += _esc("; ".join(parts) if parts else "No profile data")
        html += '\n</div>\n'

    if company:
        html += '<div class="research-block">\n<strong>Company:</strong> '
        parts = []
        if company.get("description"):
            parts.append(company["description"][:200])
        if company.get("employee_band"):
            parts.append(f"Size: {company['employee_band']}")
        if company.get("vertical"):
            parts.append(f"Vertical: {company['vertical']}")
        if company.get("known_tools"):
            tools = company["known_tools"]
            if isinstance(tools, list):
                parts.append(f"Known tools: {', '.join(tools)}")
        if company.get("recent_news"):
            parts.append(f"News: {company['recent_news'][:150]}")
        html += _esc("; ".join(parts) if parts else "No company data")
        html += '\n</div>\n'

    if signals:
        html += '<div class="research-block">\n<strong>Signals:</strong> '
        sig_text = "; ".join(s.get("description", s.get("signal_type", "")) for s in signals[:5])
        html += _esc(sig_text)
        html += '\n</div>\n'

    html += '</div>\n'
    return html


def _render_message_block(msg_id: str, label: str, msg: dict) -> str:
    subject = msg.get("subject_line", "")
    body = msg.get("body", "")
    p_score = msg.get("personalization_score")

    html = f'<div class="msg-block">\n'
    html += f'<h4>{_esc(label)}'
    if p_score:
        html += f' <span class="p-score p-score-{p_score}">P{p_score}</span>'
    html += '</h4>\n'

    if subject:
        html += f'<p class="msg-subject">Subject: {_esc(subject)}</p>\n'

    safe_id = _attr(msg_id)
    html += f'<div class="msg-body" id="{safe_id}">{_esc(body)}</div>\n'

    html += f'<button class="copy-btn" onclick="doCopy(this, \'{safe_id}\', \'body\')">Copy Message</button>\n'
    if subject:
        html += f'<button class="copy-sub" onclick="doCopy(this, \'{_attr_esc(subject)}\', \'text\')">Copy Subject</button>\n'

    html += '</div>\n'
    return html


def _render_call_snippet(msg_id: str, label: str, msg: dict) -> str:
    body = msg.get("body", "")

    html = f'<div class="msg-block call-block">\n'
    html += f'<h4>{_esc(label)}</h4>\n'

    safe_id = _attr(msg_id)
    html += f'<div class="msg-body call-body" id="{safe_id}">{_esc(body)}</div>\n'
    html += f'<button class="copy-btn" onclick="doCopy(this, \'{safe_id}\', \'body\')">Copy Script</button>\n'
    html += '</div>\n'
    return html


def _render_objection(obj: dict) -> str:
    html = '<div class="objection-block">\n'
    html += '<h4>Predicted Objection</h4>\n'
    html += f'<div class="objection-q"><strong>Likely:</strong> {_esc(obj.get("objection", ""))}</div>\n'
    html += f'<div class="objection-a"><strong>Response:</strong> {_esc(obj.get("response", ""))}</div>\n'
    html += '</div>\n'
    return html


def _render_prep_card(contact: dict, person: dict, company: dict,
                      signals: list, messages: list) -> str:
    """Render the meeting prep card (hidden by default)."""
    cid = _attr(contact["id"])
    name = f'{contact.get("first_name","")} {contact.get("last_name","")}'
    title = contact.get("title", "")
    company_name = contact.get("company_name", "")

    html = f'<div class="prep-card" id="prep-{cid}" style="display:none;">\n'
    html += '<h4>Meeting Prep</h4>\n'

    # Company snapshot
    html += '<div class="prep-section">\n<strong>Company:</strong> '
    if company:
        desc = company.get("description", company_name)
        emp = company.get("employee_band", "")
        html += f'{_esc(desc[:300])}'
        if emp:
            html += f' ({_esc(emp)} employees)'
    else:
        html += _esc(company_name)
    html += '\n</div>\n'

    # Prospect snapshot
    html += '<div class="prep-section">\n<strong>Prospect:</strong> '
    html += f'{_esc(name)}, {_esc(title)}. '
    if person:
        if person.get("about"):
            html += _esc(person["about"][:200])
        if person.get("tenure_months"):
            html += f' Tenure: {person["tenure_months"]} months.'
    html += '\n</div>\n'

    # Known tech stack
    known_tools = company.get("known_tools", []) if company else []
    if isinstance(known_tools, str):
        try:
            known_tools = json.loads(known_tools)
        except (json.JSONDecodeError, TypeError):
            known_tools = []
    if known_tools:
        html += f'<div class="prep-section">\n<strong>Known Tools:</strong> {_esc(", ".join(known_tools))}\n</div>\n'

    # Pain hypothesis
    pain = ""
    for msg in messages:
        if msg.get("pain_hook"):
            pain = msg["pain_hook"]
            break
    if pain:
        html += f'<div class="prep-section">\n<strong>Pain Hypothesis:</strong> {_esc(pain)}\n</div>\n'

    # Discovery questions
    html += '<div class="prep-section">\n<strong>Discovery Questions:</strong>\n<ol>\n'
    html += f'  <li>Walk me through how your team tests {_esc(company_name)}\'s core product workflows.</li>\n'
    html += '  <li>What does your current automation stack look like?</li>\n'
    html += '  <li>Where are regression cycles hitting hardest?</li>\n'
    html += '  <li>Is there a timeline or leadership mandate driving this?</li>\n'
    html += '</ol>\n</div>\n'

    # Relevant proof points
    proof_points_used = set()
    for msg in messages:
        pp = msg.get("proof_point_used")
        if pp:
            proof_points_used.add(pp)
    if proof_points_used:
        html += f'<div class="prep-section">\n<strong>Proof Points Used:</strong> {_esc(", ".join(proof_points_used))}\n</div>\n'

    html += f'<button class="copy-btn" onclick="copyPrepCard(\'{cid}\')">Copy Prep</button>\n'
    html += '</div>\n'
    return html


# ─── SCRIPTS ─────────────────────────────────────────────────

def _render_scripts(contacts: list) -> str:
    """Render all JS for interactivity and localStorage persistence."""
    contact_ids = json.dumps([c["id"] for c in contacts])
    return f'''<script>
// ── Contact IDs for localStorage ──
var CONTACT_IDS = {contact_ids};
var STORAGE_KEY = 'occ-batch-state';

// ── Init: restore saved state ──
(function() {{
  try {{
    var saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}');
    CONTACT_IDS.forEach(function(cid) {{
      var state = saved[cid];
      if (!state) return;
      var statusDD = document.querySelector('.status-dd[data-cid="' + cid + '"]');
      if (statusDD && state.status) {{
        statusDD.value = state.status;
        // Show prep card if Meeting Booked
        if (state.status === 'Meeting Booked') showPrep(cid);
      }}
      var replyDD = document.querySelector('.reply-dd[data-cid="' + cid + '"]');
      if (replyDD && state.reply_tag) replyDD.value = state.reply_tag;
    }});
  }} catch(e) {{}}
}})();

// ── Save state to localStorage ──
function persistState() {{
  var state = {{}};
  CONTACT_IDS.forEach(function(cid) {{
    var statusDD = document.querySelector('.status-dd[data-cid="' + cid + '"]');
    var replyDD = document.querySelector('.reply-dd[data-cid="' + cid + '"]');
    state[cid] = {{
      status: statusDD ? statusDD.value : '',
      reply_tag: replyDD ? replyDD.value : ''
    }};
  }});
  try {{ localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }} catch(e) {{}}
}}

function saveStatus(el) {{
  var cid = el.dataset.cid;
  if (el.value === 'Meeting Booked') showPrep(cid);
  else hidePrep(cid);
  persistState();
}}

function saveReplyTag(el) {{
  persistState();
}}

// ── Filtering ──
function applyFilters() {{
  var pri = document.getElementById('filterPriority').value;
  var persona = document.getElementById('filterPersona').value;
  var status = document.getElementById('filterStatus').value;

  document.querySelectorAll('.prospect-row').forEach(function(row) {{
    var show = true;
    var rowPri = parseInt(row.dataset.priority || '0');
    var rowPersona = row.dataset.persona || '';

    if (pri === '5' && rowPri < 5) show = false;
    if (pri === '4' && rowPri !== 4) show = false;
    if (pri === '45' && rowPri < 4) show = false;
    if (persona !== 'all' && rowPersona !== persona) show = false;

    if (status !== 'all') {{
      var dd = row.querySelector('.status-dd');
      if (dd && dd.value !== status) show = false;
    }}

    row.style.display = show ? '' : 'none';
  }});
}}

// ── Card toggling ──
function toggleCard(cid) {{
  var body = document.getElementById('body-' + cid);
  if (body) body.style.display = body.style.display === 'none' ? 'block' : 'none';
}}

function scrollToCard(cid) {{
  var card = document.getElementById('card-' + cid);
  if (card) {{
    card.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    var body = document.getElementById('body-' + cid);
    if (body) body.style.display = 'block';
  }}
}}

// ── Meeting prep ──
function showPrep(cid) {{
  var el = document.getElementById('prep-' + cid);
  if (el) el.style.display = 'block';
}}
function hidePrep(cid) {{
  var el = document.getElementById('prep-' + cid);
  if (el) el.style.display = 'none';
}}

// ── Copy functions ──
function doCopy(btn, val, mode) {{
  var text;
  if (mode === 'body') {{
    var el = document.getElementById(val);
    text = el ? el.innerText : val;
  }} else {{
    text = val;
  }}
  var orig = btn.textContent;
  navigator.clipboard.writeText(text).then(function() {{
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function() {{ btn.textContent = orig; btn.classList.remove('copied'); }}, 2000);
  }}).catch(function() {{
    // Fallback
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try {{ document.execCommand('copy'); }} catch(e) {{}}
    document.body.removeChild(ta);
    btn.textContent = 'Copied!';
    btn.classList.add('copied');
    setTimeout(function() {{ btn.textContent = orig; btn.classList.remove('copied'); }}, 2000);
  }});
}}

function copyPrepCard(cid) {{
  var el = document.getElementById('prep-' + cid);
  if (!el) return;
  var text = el.innerText;
  navigator.clipboard.writeText(text).then(function() {{
    var btn = el.querySelector('.copy-btn');
    if (btn) {{
      btn.textContent = 'Copied!';
      btn.classList.add('copied');
      setTimeout(function() {{ btn.textContent = 'Copy Prep'; btn.classList.remove('copied'); }}, 2000);
    }}
  }});
}}
</script>'''


# ─── CSS ─────────────────────────────────────────────────────

def _get_css() -> str:
    return '''* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f7fa; color: #1a1a2e; line-height: 1.6; padding: 20px; }
.container { max-width: 1200px; margin: 0 auto; }
h1 { font-size: 1.8rem; color: #1a1a2e; margin-bottom: 4px; }
.subtitle { color: #666; font-size: 0.95rem; margin-bottom: 20px; }
.section-title { font-size: 1.3rem; color: #1a1a2e; margin: 30px 0 15px; border-bottom: 2px solid #4361ee; padding-bottom: 6px; }

/* Pre-brief */
.pre-brief { background: #eef2ff; border-left: 4px solid #4361ee; padding: 16px 20px; border-radius: 8px; margin-bottom: 20px; }
.pre-brief h3 { font-size: 1rem; color: #4361ee; margin-bottom: 8px; }
.pre-brief li { font-size: 0.88rem; margin-bottom: 4px; color: #333; }

/* Stats */
.stats { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 20px; }
.stat-box { background: #fff; padding: 12px 18px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); min-width: 110px; }
.stat-num { font-size: 1.4rem; font-weight: 700; color: #4361ee; }
.stat-label { font-size: 0.75rem; color: #888; }

/* A/B info */
.ab-info { background: #fff7ed; border-left: 4px solid #f59e0b; padding: 10px 16px; border-radius: 6px; margin-bottom: 20px; font-size: 0.88rem; }

/* Filters */
.filter-bar { background: #fff; padding: 12px 16px; border-radius: 8px; margin-bottom: 20px; display: flex; gap: 20px; flex-wrap: wrap; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.filter-bar label { font-size: 0.82rem; color: #555; }
.filter-bar select { padding: 4px 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 0.82rem; }

/* Tracker table */
.table-wrap { overflow-x: auto; margin-bottom: 30px; }
table { width: 100%; border-collapse: collapse; font-size: 0.8rem; background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
th { background: #4361ee; color: #fff; padding: 8px 10px; text-align: left; font-weight: 600; white-space: nowrap; }
td { padding: 6px 10px; border-bottom: 1px solid #eee; vertical-align: top; }
tr:hover { background: #f0f4ff; }
.url-cell { font-size: 0.72rem; word-break: break-all; max-width: 100px; }
.name-cell a { font-weight: 600; }
.ab-cell { font-weight: 600; font-size: 0.85rem; }
.status-dd, .reply-dd { font-size: 0.75rem; padding: 3px 5px; border: 1px solid #ddd; border-radius: 4px; max-width: 130px; }

/* Badges */
.badge { display: inline-block; padding: 2px 7px; border-radius: 10px; font-size: 0.68rem; font-weight: 600; margin: 1px 2px; white-space: nowrap; }
.badge-qa { background: #d4edda; color: #155724; }
.badge-vp { background: #d6eaf8; color: #1a5276; }
.badge-inf { background: #e8f5e9; color: #2e7d32; }
.badge-bi { background: #ffeaa7; color: #856404; }
.badge-fin { background: #e8daef; color: #6c3483; }
.badge-tech { background: #fce4ec; color: #880e4f; }
.badge-health { background: #e0f7fa; color: #00695c; }
.badge-ecom { background: #fff3e0; color: #e65100; }
.badge-tel { background: #e3f2fd; color: #1565c0; }
.badge-other { background: #f5f5f5; color: #616161; }

/* Priority badges */
.pri-badge { display: inline-block; width: 26px; height: 26px; line-height: 26px; text-align: center; border-radius: 50%; font-weight: 700; font-size: 0.82rem; color: #fff; }
.pri-hot { background: #e74c3c; }
.pri-warm { background: #f39c12; }
.pri-std { background: #3498db; }
.pri-low { background: #95a5a6; }

/* Personalization score */
.p-score { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.72rem; font-weight: 700; }
.p-score-3 { background: #d4edda; color: #155724; }
.p-score-2 { background: #fff3cd; color: #856404; }
.p-score-1 { background: #f8d7da; color: #721c24; }

/* Prospect cards */
.card { background: #fff; border-radius: 10px; margin-bottom: 14px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); border-left: 4px solid #4361ee; overflow: hidden; }
.card-header { padding: 14px 20px; cursor: pointer; }
.card-header:hover { background: #f8f9ff; }
.card-header h3 { font-size: 1rem; color: #1a1a2e; margin-bottom: 2px; display: flex; align-items: center; gap: 8px; }
.card-meta { font-size: 0.82rem; color: #888; }
.card-body { padding: 0 20px 20px; }

/* Research */
.research-section { background: #fafbfc; padding: 14px; border-radius: 6px; margin-bottom: 14px; border: 1px solid #eee; }
.research-section h4 { font-size: 0.88rem; color: #4361ee; margin-bottom: 8px; }
.research-block { font-size: 0.82rem; color: #555; margin-bottom: 6px; line-height: 1.5; }

/* Message blocks */
.msg-block { margin-bottom: 16px; padding: 14px; background: #fafbfc; border-radius: 6px; border: 1px solid #eee; }
.msg-block h4 { font-size: 0.88rem; color: #4361ee; margin-bottom: 6px; }
.msg-subject { font-weight: 600; color: #1a1a2e; margin-bottom: 6px; font-size: 0.88rem; }
.msg-body { font-size: 0.85rem; color: #333; white-space: pre-line; line-height: 1.6; padding: 10px 14px; background: #fff; border-radius: 4px; border: 1px solid #eee; }
.call-block { border-left: 3px solid #27ae60; }
.call-body { background: #f0fdf4; }
.copy-btn { background: #4361ee; color: #fff; border: none; padding: 5px 12px; border-radius: 5px; cursor: pointer; font-size: 0.75rem; margin-top: 6px; margin-right: 6px; }
.copy-btn:hover { background: #3a56d4; }
.copy-btn.copied { background: #27ae60; }
.copy-sub { background: #e0e7ff; color: #4361ee; border: 1px solid #c7d2fe; padding: 4px 10px; border-radius: 5px; cursor: pointer; font-size: 0.75rem; margin-top: 6px; }
.copy-sub:hover { background: #c7d2fe; }
.copy-sub.copied { background: #27ae60; color: #fff; border-color: #27ae60; }

/* Objection */
.objection-block { margin-bottom: 14px; padding: 14px; background: #fff8f0; border-radius: 6px; border: 1px solid #fde68a; }
.objection-block h4 { font-size: 0.88rem; color: #d97706; margin-bottom: 6px; }
.objection-q { font-size: 0.85rem; margin-bottom: 6px; }
.objection-a { font-size: 0.85rem; color: #555; }

/* Prep card */
.prep-card { margin-top: 14px; padding: 16px; background: #eef2ff; border-radius: 8px; border: 2px solid #4361ee; }
.prep-card h4 { font-size: 1rem; color: #4361ee; margin-bottom: 10px; }
.prep-section { font-size: 0.85rem; margin-bottom: 8px; line-height: 1.5; }
.prep-section ol { margin-left: 20px; margin-top: 4px; }
.prep-section li { margin-bottom: 3px; }

/* Links */
a { color: #4361ee; text-decoration: none; }
a:hover { text-decoration: underline; }

/* Responsive */
@media (max-width: 768px) {
  .stats { flex-direction: column; }
  .filter-bar { flex-direction: column; gap: 8px; }
  .card-header h3 { font-size: 0.92rem; }
}'''


# ─── UTILITIES ───────────────────────────────────────────────

def _esc(text) -> str:
    """HTML-escape text for safe rendering."""
    if not text:
        return ""
    s = str(text)
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _attr(text) -> str:
    """Escape for use in HTML attributes."""
    if not text:
        return ""
    s = str(text)
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&#39;")


def _attr_esc(text) -> str:
    """Escape text for embedding in JS string inside onclick attribute."""
    if not text:
        return ""
    s = str(text)
    return s.replace("\\", "\\\\").replace("'", "\\'").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")
