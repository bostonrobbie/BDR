"""
Memory Classifier - Automatically categorizes raw files into memory types.

Reads file content and determines whether it's a call note, win report,
loss report, competitor intel, market intel, or unknown. Uses keyword
scoring with section-header detection for high accuracy.
"""

import os
import re
from typing import Optional


# ─── CLASSIFICATION CATEGORIES ───────────────────────────────

CATEGORIES = {
    "call_note": {
        "destination": "call-notes",
        "strong_signals": [
            r"call\s*(notes?|log|summary|recap)",
            r"(cold\s*call|discovery\s*call|follow[- ]?up\s*call)",
            r"\*\*call\s*type\*\*",
            r"\*\*duration\*\*",
            r"\*\*outcome\*\*.*?(connected|voicemail|no.?answer|meeting.?booked)",
            r"what\s+they\s+said",
            r"their\s+stack",
            r"their\s+pain",
            r"objections?\s+raised",
            r"next\s+steps",
        ],
        "weak_signals": [
            r"(spoke|talked|called|dialed|reached)\s+(with|to|him|her|them)",
            r"(left\s+voicemail|got\s+through|connected)",
            r"(they\s+mentioned|they\s+said|they\s+use|he\s+mentioned|she\s+mentioned)",
            r"(follow\s*up|callback|scheduled|following\s+up)",
            r"on\s+the\s+(phone|call)",
            r"(seemed\s+interested|asked\s+me\s+to|send\s+more\s+info)",
            r"(called\s+\w+\s+\w+\s+at|spoke\s+with\s+\w+)",
            r"(they.?re\s+using|they\s+have|their\s+team)",
            r"(worried\s+about|concerned\s+about|struggling\s+with)",
        ],
        "anti_signals": [
            r"(won|closed|deal\s+closed|signed)",
            r"(lost|didn.?t\s+close|walked\s+away)",
        ],
    },
    "win": {
        "destination": "wins",
        "strong_signals": [
            r"win\s*report",
            r"(date\s*closed|deal\s*closed|closed[- ]?won)",
            r"how\s+they\s+found\s+us",
            r"what\s+resonated",
            r"decision\s+process",
            r"what\s+accelerated",
            r"\*\*ae\*\*",
            r"(signed|converted|deal\s*won|closed\s*the\s*deal)",
        ],
        "weak_signals": [
            r"(proof\s+point\s+that\s+landed|capability\s+that\s+mattered)",
            r"(roi\s+angle|what\s+worked)",
            r"(champion|decision\s+maker|influencer)",
            r"(trial\s+results?|poc\s+results?)",
        ],
        "anti_signals": [
            r"(lost|didn.?t\s+close|walked\s+away|not\s+interested)",
            r"loss\s*report",
        ],
    },
    "loss": {
        "destination": "losses",
        "strong_signals": [
            r"loss\s*report",
            r"(date\s*lost|deal\s*lost|closed[- ]?lost)",
            r"why\s+we\s+lost",
            r"what\s+we\s+could\s+have\s+done\s+differently",
            r"signals?\s+we\s+missed",
            r"re[- ]?engagement\s+potential",
            r"objections?\s+we\s+didn.?t\s+overcome",
        ],
        "weak_signals": [
            r"(chose\s+competitor|went\s+with\s+another|picked\s+\w+\s+instead)",
            r"(no\s+budget|no\s+urgency|champion\s+left)",
            r"(walked\s+away|went\s+dark|ghosted)",
            r"(what\s+killed|almost\s+killed|deal\s+breaker)",
        ],
        "anti_signals": [
            r"(won|closed[- ]?won|signed|converted)",
            r"win\s*report",
        ],
    },
    "competitor": {
        "destination": "competitors",
        "strong_signals": [
            r"battle\s*card",
            r"(displacement|competitive)\s+(angles?|analysis|comparison|positioning)",
            r"where\s+\w+\s+(falls\s+short|is\s+weak|struggles)",
            r"(pricing\s+context|talk\s+track)",
            r"common\s+objections?\s+when\s+displacing",
        ],
        "weak_signals": [
            r"(selenium|cypress|playwright|katalon|tosca|mabl|testim|uft|browserstack|appium)",
            r"(competitor|vs\.?|versus|compared\s+to|alternative)",
            r"(their\s+weakness|our\s+advantage|differentiat)",
        ],
        "anti_signals": [],
    },
    "market_intel": {
        "destination": "market-intel",
        "strong_signals": [
            r"(market|industry)\s+(trend|landscape|analysis|overview|report)",
            r"(analyst|gartner|forrester|g2)\s+(coverage|report|wave|quadrant)",
            r"(market\s+size|\btam\b|\bsam\b|\bsom\b)",
            r"(competitive\s+landscape|vendor\s+landscape)",
            r"competitor\s+moves",
        ],
        "weak_signals": [
            r"(market\s+trend|industry\s+forecast|market\s+prediction|market\s+outlook)",
            r"(funding\s+round|acquisition\s+of|merger\s+with|ipo\s+filing)",
            r"(regulatory\s+change|compliance\s+mandate)",
            r"(market\s+growing|market\s+declining|emerging\s+category)",
        ],
        "anti_signals": [],
    },
}

# Minimum score thresholds
STRONG_WEIGHT = 3
WEAK_WEIGHT = 1
ANTI_WEIGHT = -4
CONFIDENCE_THRESHOLD = 3  # Minimum score to classify


def classify_file(filepath: str, content: str = None) -> dict:
    """Classify a file into a memory category.

    Args:
        filepath: Path to the file.
        content: Optional pre-read content. If None, reads from filepath.

    Returns:
        Dict with:
            category: str - The detected category (or "unknown")
            destination: str - Target subdirectory in memory/
            confidence: float - Score confidence (0-1)
            scores: dict - Raw scores per category
            signals_matched: list - Which signals triggered the classification
    """
    if content is None:
        with open(filepath, "r", errors="replace") as f:
            content = f.read()

    filename = os.path.basename(filepath).lower()
    text = content.lower()

    scores = {}
    matched_signals = {}

    for cat_name, cat_config in CATEGORIES.items():
        score = 0
        matched = []

        # Filename bonus
        if cat_name.replace("_", "") in filename or cat_name.replace("_", "-") in filename:
            score += STRONG_WEIGHT
            matched.append(f"filename:{filename}")

        # Strong signals
        for pattern in cat_config["strong_signals"]:
            if re.search(pattern, text, re.IGNORECASE):
                score += STRONG_WEIGHT
                matched.append(f"strong:{pattern}")

        # Weak signals
        for pattern in cat_config["weak_signals"]:
            if re.search(pattern, text, re.IGNORECASE):
                score += WEAK_WEIGHT
                matched.append(f"weak:{pattern}")

        # Anti-signals (reduce score)
        for pattern in cat_config["anti_signals"]:
            if re.search(pattern, text, re.IGNORECASE):
                score += ANTI_WEIGHT
                matched.append(f"anti:{pattern}")

        scores[cat_name] = max(score, 0)
        matched_signals[cat_name] = matched

    # Find the winner
    if not scores or max(scores.values()) < CONFIDENCE_THRESHOLD:
        return {
            "category": "unknown",
            "destination": "inbox",
            "confidence": 0.0,
            "scores": scores,
            "signals_matched": [],
        }

    best_cat = max(scores, key=scores.get)
    best_score = scores[best_cat]

    # Normalize confidence to 0-1 range (max reasonable score ~20)
    confidence = min(best_score / 15.0, 1.0)

    return {
        "category": best_cat,
        "destination": CATEGORIES[best_cat]["destination"],
        "confidence": round(confidence, 2),
        "scores": scores,
        "signals_matched": matched_signals.get(best_cat, []),
    }


def classify_content_type(filepath: str) -> str:
    """Detect the file format type.

    Returns: 'markdown', 'csv', 'json', 'text', or 'unknown'.
    """
    ext = os.path.splitext(filepath)[1].lower()
    if ext in (".md", ".markdown"):
        return "markdown"
    if ext == ".csv":
        return "csv"
    if ext == ".json":
        return "json"
    if ext in (".txt", ".text", ".log"):
        return "text"
    return "unknown"


def extract_metadata_from_content(content: str) -> dict:
    """Extract structured metadata from free-form content.

    Pulls out names, companies, dates, tools mentioned, and pain signals.
    """
    metadata = {}

    # Date patterns
    date_match = re.search(r"(\d{4}-\d{2}-\d{2})", content)
    if date_match:
        metadata["date"] = date_match.group(1)

    # Name at company pattern: "Name at Company" or "Name - Company"
    name_co = re.search(
        r"(?:^#\s*(?:Call Notes|Win Report|Loss Report)[:\s]*)"
        r"([A-Z][a-z]+\s+[A-Z][a-z]+)\s+(?:at|@|-)\s+([A-Za-z0-9\s]+)",
        content, re.MULTILINE
    )
    if name_co:
        metadata["person_name"] = name_co.group(1).strip()
        metadata["company_name"] = name_co.group(2).strip()

    # Prospect/company from bold fields
    for pattern, key in [
        (r"\*\*Prospect:\*\*\s*(.+)", "person_name"),
        (r"\*\*Company:\*\*\s*(.+)", "company_name"),
        (r"\*\*Company\s*(?:Name)?:\*\*\s*(.+)", "company_name"),
        (r"\*\*Vertical:\*\*\s*(.+)", "vertical"),
        (r"\*\*AE:\*\*\s*(.+)", "ae"),
    ]:
        match = re.search(pattern, content, re.IGNORECASE)
        if match and key not in metadata:
            metadata[key] = match.group(1).strip()

    # Tools mentioned
    tools = set()
    tool_names = [
        "selenium", "cypress", "playwright", "katalon", "tosca", "mabl",
        "testim", "uft", "appium", "browserstack", "sauce labs", "ranorex",
        "testcomplete", "qtp", "jira", "testrail", "jenkins", "github actions",
    ]
    content_lower = content.lower()
    for tool in tool_names:
        if tool in content_lower:
            tools.add(tool)
    if tools:
        metadata["tools_mentioned"] = sorted(tools)

    # Pain signals
    pain_keywords = {
        "maintenance": ["maintenance", "flaky", "brittle", "breaking", "broken tests"],
        "velocity": ["slow", "velocity", "release", "regression cycle", "bottleneck", "ci/cd"],
        "coverage": ["coverage", "manual testing", "can't keep up", "falling behind"],
        "cost": ["budget", "expensive", "cost", "roi", "spending"],
        "scaling": ["scale", "scaling", "growing", "headcount", "team size"],
    }
    pains = []
    for pain, keywords in pain_keywords.items():
        if any(kw in content_lower for kw in keywords):
            pains.append(pain)
    if pains:
        metadata["pain_signals"] = pains

    return metadata
