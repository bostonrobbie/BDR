"""Analytics routes."""

from fastapi import APIRouter

from src.db import models

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/replies")
def reply_analytics():
    return models.get_reply_analytics()


@router.get("/pipeline")
def pipeline_analytics():
    conn = models.get_db()
    funnel = {
        "total_prospects": conn.execute("SELECT COUNT(*) FROM contacts WHERE status='active'").fetchone()[0],
        "touched": conn.execute("SELECT COUNT(*) FROM contacts WHERE stage NOT IN ('new')").fetchone()[0],
        "replied": conn.execute("SELECT COUNT(DISTINCT contact_id) FROM replies").fetchone()[0],
        "meetings": conn.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0],
        "opportunities": conn.execute("SELECT COUNT(*) FROM opportunities WHERE opportunity_created=1").fetchone()[0],
    }
    if funnel["touched"] > 0:
        funnel["reply_rate"] = round(funnel["replied"] / funnel["touched"] * 100, 1)
    else:
        funnel["reply_rate"] = 0
    if funnel["replied"] > 0:
        funnel["meeting_rate"] = round(funnel["meetings"] / funnel["replied"] * 100, 1)
    else:
        funnel["meeting_rate"] = 0
    if funnel["meetings"] > 0:
        funnel["opp_rate"] = round(funnel["opportunities"] / funnel["meetings"] * 100, 1)
    else:
        funnel["opp_rate"] = 0
    conn.close()
    return funnel


@router.get("/experiments")
def experiment_analytics():
    conn = models.get_db()
    rows = conn.execute("SELECT * FROM experiments ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.get("/batch-comparison")
def batch_comparison():
    """Cross-batch comparison for intelligence charts."""
    conn = models.get_db()
    batches = conn.execute("""
        SELECT b.id, b.batch_number, b.ab_variable, b.ab_description, b.created_at,
               (SELECT COUNT(*) FROM batch_prospects WHERE batch_id=b.id) as prospects,
               (SELECT COUNT(*) FROM message_drafts WHERE batch_id=b.id) as messages,
               (SELECT COUNT(*) FROM message_drafts WHERE batch_id=b.id AND qc_passed=1) as qc_passed,
               (SELECT COUNT(DISTINCT r.contact_id) FROM replies r
                JOIN batch_prospects bp ON r.contact_id=bp.contact_id
                WHERE bp.batch_id=b.id) as replies,
               (SELECT COUNT(*) FROM opportunities o
                JOIN contacts c ON o.contact_id=c.id
                JOIN batch_prospects bp ON c.id=bp.contact_id
                WHERE bp.batch_id=b.id) as meetings,
               (SELECT AVG(md.personalization_score) FROM message_drafts md
                WHERE md.batch_id=b.id AND md.personalization_score > 0) as avg_personalization
        FROM batches b ORDER BY b.batch_number ASC
    """).fetchall()
    conn.close()
    results = []
    for b in batches:
        d = dict(b)
        d["reply_rate"] = round(d["replies"] / d["prospects"] * 100, 1) if d["prospects"] > 0 else 0
        d["meeting_rate"] = round(d["meetings"] / d["replies"] * 100, 1) if d["replies"] > 0 else 0
        d["qc_pass_rate"] = round(d["qc_passed"] / d["messages"] * 100, 1) if d["messages"] > 0 else 0
        d["avg_personalization"] = round(d["avg_personalization"] or 0, 1)
        results.append(d)
    return results


@router.get("/top-messages")
def top_messages():
    """Top performing messages (those that got replies)."""
    conn = models.get_db()
    rows = conn.execute("""
        SELECT md.id, md.contact_id, md.touch_number, md.channel, md.subject_line,
               md.body as message_body, md.personalization_score, md.ab_group,
               c.first_name, c.last_name, c.persona_type, c.title,
               a.name as company,
               r.reply_tag, r.summary as reply_summary
        FROM message_drafts md
        JOIN contacts c ON md.contact_id = c.id
        LEFT JOIN accounts a ON c.account_id = a.id
        LEFT JOIN replies r ON r.contact_id = md.contact_id
        WHERE r.id IS NOT NULL
        ORDER BY md.personalization_score DESC, r.created_at DESC
        LIMIT 10
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.get("/token-costs")
def token_costs():
    """Token usage and cost tracking."""
    conn = models.get_db()

    by_agent = conn.execute("""
        SELECT agent_name,
               COUNT(*) as runs,
               SUM(tokens_used) as total_tokens,
               AVG(tokens_used) as avg_tokens,
               SUM(duration_ms) as total_duration_ms
        FROM agent_runs
        GROUP BY agent_name
        ORDER BY total_tokens DESC
    """).fetchall()

    by_batch = conn.execute("""
        SELECT b.batch_number,
               (SELECT COUNT(*) FROM batch_prospects WHERE batch_id=b.id) as prospects,
               (SELECT SUM(ar.tokens_used) FROM agent_runs ar
                WHERE ar.run_type LIKE '%batch%' OR ar.batch_id=b.id) as batch_tokens
        FROM batches b ORDER BY b.batch_number ASC
    """).fetchall()

    totals = conn.execute("""
        SELECT COUNT(*) as total_runs,
               SUM(tokens_used) as total_tokens,
               SUM(duration_ms) as total_duration_ms
        FROM agent_runs
    """).fetchone()

    prospect_count = conn.execute("SELECT COUNT(*) FROM contacts WHERE status='active'").fetchone()[0]
    reply_count = conn.execute("SELECT COUNT(DISTINCT contact_id) FROM replies").fetchone()[0]

    conn.close()

    cost_rate = 3.0

    agent_results = []
    for r in by_agent:
        d = dict(r)
        d["est_cost_usd"] = round((d["total_tokens"] or 0) / 1_000_000 * cost_rate, 4)
        agent_results.append(d)

    batch_results = []
    for b in by_batch:
        d = dict(b)
        tokens = d.get("batch_tokens") or 0
        prospects = d.get("prospects") or 0
        d["est_cost_usd"] = round(tokens / 1_000_000 * cost_rate, 4)
        d["cost_per_prospect"] = round(d["est_cost_usd"] / prospects, 4) if prospects > 0 else 0
        batch_results.append(d)

    total_tokens = (totals["total_tokens"] or 0) if totals else 0
    total_cost = round(total_tokens / 1_000_000 * cost_rate, 4)

    return {
        "by_agent": agent_results,
        "by_batch": batch_results,
        "totals": {
            "total_runs": (totals["total_runs"] or 0) if totals else 0,
            "total_tokens": total_tokens,
            "total_duration_ms": (totals["total_duration_ms"] or 0) if totals else 0,
            "est_cost_usd": total_cost,
            "cost_per_prospect": round(total_cost / prospect_count, 4) if prospect_count > 0 else 0,
            "cost_per_reply": round(total_cost / reply_count, 4) if reply_count > 0 else 0,
            "prospect_count": prospect_count,
            "reply_count": reply_count,
        }
    }
