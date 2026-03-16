#!/usr/bin/env python3
"""
Parses touch2_business_pressure_mar9.md and generates touch2-review-viewer.html
"""
import re, json

MD_PATH  = r'C:\Users\User\Desktop\Work\touch2_business_pressure_mar9.md'
OUT_PATH = r'C:\Users\User\Desktop\Work\touch2-review-viewer.html'

# ── Read source file ─────────────────────────────────────────────────────────
with open(MD_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Strip trailing footer summary (appears after the last contact section)
content = re.sub(r'\n## Special Handling Summary.*$', '', content, flags=re.DOTALL)

# ── Split into per-contact sections ─────────────────────────────────────────
sections = re.split(r'\n(?=### #\d+)', content)

emails = []
for section in sections:
    m = re.match(r'### #(\d+)\s+-+\s+(.+?)\s+@\s+(.+?)(?:\n|$)', section)
    if not m:
        continue
    num     = int(m.group(1))
    name    = m.group(2).strip()
    company = m.group(3).strip()

    is_dnc     = ('DNC' in section and 'GMAIL' not in section and 'SEQUENCING' not in section and 'Proof Point' not in section)
    is_gmail   = 'GMAIL-ONLY' in section
    is_seqflag = 'SEQUENCING FLAG' in section

    if is_dnc:
        emails.append({'num': num, 'name': name, 'company': company,
                       'send': 'dnc', 'proof': '', 'subject': '', 'body': '', 'flag': 'dnc'})
        continue

    proof_m = re.search(r'T2 Proof Point:\s*(.+?)$', section, re.MULTILINE)
    proof   = proof_m.group(1).strip() if proof_m else ''

    subj_m  = re.search(r'\*\*Subject:\*\*\s*(.+?)$', section, re.MULTILINE)
    subject = subj_m.group(1).strip() if subj_m else ''

    body_m  = re.search(r'\*\*Subject:\*\*[^\n]*\n(.*?)(?:\n---|\Z)', section, re.DOTALL)
    body    = body_m.group(1).strip() if body_m else ''

    send = 'gmail' if is_gmail else 'apollo'
    flag = ''
    if is_gmail:   flag = 'gmail'
    if is_seqflag: flag = 'seqflag'

    emails.append({'num': num, 'name': name, 'company': company,
                   'send': send, 'proof': proof, 'subject': subject,
                   'body': body, 'flag': flag})

emails.sort(key=lambda e: e['num'])

print(f"Parsed {len(emails)} entries")
for e in emails:
    print(f"  #{e['num']:>2}  {e['name']:<30} @ {e['company']:<35} | {e['send']:<6} | {e['proof']}")

# ── Build HTML ────────────────────────────────────────────────────────────────
emails_json = json.dumps(emails, ensure_ascii=False, indent=2)

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Touch 2 Review — Business Pressure Formula</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#f0f2f5;color:#1a1a2e}
.approve-banner{background:#fff3cd;border-bottom:2px solid #f0ad4e;padding:12px 24px;text-align:center;font-weight:600;font-size:14px;color:#856404;position:sticky;top:0;z-index:100}
.header{background:#1a1a2e;color:white;padding:20px 24px}
.header h1{font-size:20px;margin-bottom:6px}
.header p{font-size:13px;opacity:.7}
.stats-bar{display:flex;gap:16px;padding:12px 24px;background:white;border-bottom:1px solid #e0e0e0;flex-wrap:wrap}
.stat{font-size:12px;color:#555}.stat strong{color:#1a1a2e}
.stat.pass{color:#2d6a4f;font-weight:600}
.flags-section{padding:12px 24px;background:#fff8e1;border-bottom:1px solid #ffe082}
.flags-section h3{font-size:12px;text-transform:uppercase;letter-spacing:.5px;color:#795548;margin-bottom:8px}
.flag-item{font-size:13px;color:#5d4037;margin-bottom:4px}
.controls{padding:12px 24px;background:white;border-bottom:1px solid #e0e0e0;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.controls input,.controls select{padding:7px 11px;border:1px solid #ddd;border-radius:6px;font-size:13px}
.controls input{min-width:220px}
.controls button{padding:7px 14px;background:#e0e0e0;border:none;border-radius:6px;cursor:pointer;font-size:13px}
.controls button:hover{background:#d0d0d0}
.count-display{font-size:13px;color:#666;margin-left:auto}
.cards-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(480px,1fr));gap:16px;padding:20px 24px}
.card{background:white;border-radius:10px;box-shadow:0 1px 4px rgba(0,0,0,.08);overflow:hidden}
.card.dnc{opacity:.5}
.card.seqflag{border:2px solid #ff9800}
.card-header{padding:12px 16px;background:#f8f9fa;border-bottom:1px solid #eee;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.card-num{font-size:11px;color:#999;font-weight:600}
.card-name{font-size:14px;font-weight:700;color:#1a1a2e;flex:1}
.card-company{font-size:12px;color:#666}
.badge{display:inline-block;padding:2px 8px;border-radius:12px;font-size:11px;font-weight:600}
.badge-apollo{background:#e3f2fd;color:#1565c0}
.badge-gmail{background:#fce4ec;color:#c62828}
.badge-dnc{background:#eee;color:#757575}
.badge-seqflag{background:#fff3e0;color:#e65100}
.badge-CRED{background:#e8eaf6;color:#283593}
.badge-Medibuddy{background:#e8f5e9;color:#1b5e20}
.badge-Hansard{background:#fce4ec;color:#880e4f}
.badge-NagraDTV{background:#f3e5f5;color:#4a148c}
.badge-UKGov{background:#e0f7fa;color:#006064}
.card-body{padding:14px 16px}
.subject-row{display:flex;align-items:center;gap:8px;margin-bottom:10px}
.subject-label{font-size:11px;font-weight:600;color:#888;text-transform:uppercase;white-space:nowrap}
.subject-text{font-size:13px;color:#1a1a2e;font-weight:500;flex:1}
.email-body{font-size:12px;line-height:1.6;color:#444;background:#f8f9fa;border-radius:6px;padding:12px;max-height:300px;overflow-y:auto;white-space:pre-wrap;font-family:'Courier New',monospace;margin-bottom:10px}
.btn-row{display:flex;gap:8px;flex-wrap:wrap}
.btn-copy{padding:6px 14px;border:1px solid #ddd;border-radius:6px;background:white;cursor:pointer;font-size:12px;color:#333;transition:all .15s}
.btn-copy:hover{background:#f0f7ff;border-color:#1565c0;color:#1565c0}
.btn-copy.copied{background:#e8f5e9;border-color:#2e7d32;color:#2e7d32}
.no-results{grid-column:1/-1;text-align:center;padding:40px;color:#888;font-size:14px}
</style>
</head>
<body>

<div class="approve-banner">
  &#9888;&#65039; DRAFTS ONLY &mdash; Do not send until Rob replies <strong>APPROVE SEND</strong> in chat
</div>

<div class="header">
  <h1>Touch 2 Review &mdash; Business Pressure Formula</h1>
  <p>Mar 9, 2026 &middot; All 66 drafts &middot; QA Gate: ALL PASS</p>
</div>

<div class="stats-bar">
  <div class="stat">Apollo sends: <strong>62</strong></div>
  <div class="stat">Gmail-only: <strong>4</strong></div>
  <div class="stat">DNC: <strong>1</strong></div>
  <div class="stat">Seq flag: <strong>1</strong></div>
  <div class="stat">Total entries: <strong>67</strong></div>
  <div class="stat pass">&#10003; QA Gate: ALL 66 PASS</div>
</div>

<div class="flags-section">
  <h3>&#9873; Special Handling</h3>
  <div class="flag-item">&#128231; <strong>GMAIL-ONLY (#1, #3, #9, #12):</strong> Andy Nelsen, Eduardo Menezes, Hibatullah Ahmed, Amir Aly &mdash; send manually via Gmail (robert.gorham@testsigma.com), then mark Apollo Step 2 complete</div>
  <div class="flag-item">&#128683; <strong>DNC (#8):</strong> Tom Yang &mdash; No draft. No further contact.</div>
  <div class="flag-item">&#9888;&#65039; <strong>SEQUENCING FLAG (#65):</strong> Davor Milosevic &mdash; T3 sent Mar 7 before T2. Rob to decide: send as late T2, skip, or treat as re-engagement.</div>
</div>

<div class="controls">
  <input type="text" id="searchInput" placeholder="Search name, company, subject, body&hellip;" oninput="filterCards()">
  <select id="sendFilter" onchange="filterCards()">
    <option value="">All send methods</option>
    <option value="apollo">Apollo only</option>
    <option value="gmail">Gmail only</option>
    <option value="dnc">DNC</option>
    <option value="seqflag">Seq flag</option>
  </select>
  <select id="proofFilter" onchange="filterCards()">
    <option value="">All proof points</option>
    <option value="CRED">CRED</option>
    <option value="Medibuddy">Medibuddy</option>
    <option value="Hansard">Hansard</option>
    <option value="Nagra DTV">Nagra DTV</option>
    <option value="UK Gov">UK Gov</option>
  </select>
  <button onclick="clearFilters()">Clear filters</button>
  <span class="count-display" id="countDisplay">Showing all 67 entries</span>
</div>

<div class="cards-grid" id="cardsGrid"></div>

<script>
const emails = ''' + emails_json + ''';

function proofBadgeClass(proof) {
  if (!proof) return '';
  if (proof.includes('CRED')) return 'badge-CRED';
  if (proof.includes('Medibuddy') || proof.includes('MediBuddy')) return 'badge-Medibuddy';
  if (proof.includes('Hansard')) return 'badge-Hansard';
  if (proof.includes('Nagra')) return 'badge-NagraDTV';
  if (proof.includes('UK') || proof.includes('Gov')) return 'badge-UKGov';
  return '';
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function renderCards(list) {
  const grid = document.getElementById('cardsGrid');
  document.getElementById('countDisplay').textContent =
    'Showing ' + list.length + ' of ' + emails.length + ' entries';

  if (list.length === 0) {
    grid.innerHTML = '<div class="no-results">No emails match your filters.</div>';
    return;
  }

  grid.innerHTML = list.map(function(e, idx) {
    if (e.send === 'dnc') {
      return '<div class="card dnc" data-num="' + e.num + '">' +
        '<div class="card-header">' +
        '<span class="card-num">#' + e.num + '</span>' +
        '<span class="card-name">' + escHtml(e.name) + '</span>' +
        '<span class="card-company">' + escHtml(e.company) + '</span>' +
        '<span class="badge badge-dnc">DNC</span>' +
        '</div>' +
        '<div class="card-body"><p style="color:#999;font-size:13px">No draft &mdash; Do Not Contact</p></div>' +
        '</div>';
    }

    const sendBadge = e.send === 'gmail' ? 'badge-gmail' : 'badge-apollo';
    const sendLabel = e.send === 'gmail' ? 'GMAIL' : 'APOLLO';
    const seqBadge  = e.flag === 'seqflag'
      ? '<span class="badge badge-seqflag">SEQ FLAG</span>' : '';
    const proofBadge = e.proof
      ? '<span class="badge ' + proofBadgeClass(e.proof) + '">' + escHtml(e.proof) + '</span>' : '';

    const cardIdx = idx;

    return '<div class="card ' + e.flag + '" data-num="' + e.num + '">' +
      '<div class="card-header">' +
      '<span class="card-num">#' + e.num + '</span>' +
      '<span class="card-name">' + escHtml(e.name) + '</span>' +
      '<span class="card-company">' + escHtml(e.company) + '</span>' +
      '<span class="badge ' + sendBadge + '">' + sendLabel + '</span>' +
      proofBadge + seqBadge +
      '</div>' +
      '<div class="card-body">' +
      '<div class="subject-row">' +
      '<span class="subject-label">Subject</span>' +
      '<span class="subject-text">' + escHtml(e.subject) + '</span>' +
      '<button class="btn-copy" onclick="copyIdx(' + cardIdx + ',\'subj\')">Copy subject</button>' +
      '</div>' +
      '<div class="email-body">' + escHtml(e.body) + '</div>' +
      '<div class="btn-row">' +
      '<button class="btn-copy" onclick="copyIdx(' + cardIdx + ',\'full\')">&#128203; Copy full email</button>' +
      '<button class="btn-copy" onclick="copyIdx(' + cardIdx + ',\'body\')">Copy body only</button>' +
      '</div>' +
      '</div>' +
      '</div>';
  }).join('');
}

// Store filtered list globally so copy by index works
var _rendered = emails.slice();

function copyIdx(idx, part) {
  var e = _rendered[idx];
  var text = part === 'subj' ? e.subject
           : part === 'full' ? 'Subject: ' + e.subject + '\\n\\n' + e.body
           : e.body;
  var btn = event.target;
  navigator.clipboard.writeText(text).then(function() {
    btn.textContent = '\\u2705 Copied!';
    btn.classList.add('copied');
    setTimeout(function() { btn.classList.remove('copied'); btn.textContent = part === 'subj' ? 'Copy subject' : part === 'full' ? '\\uD83D\\uDCCB Copy full email' : 'Copy body only'; }, 1500);
  }).catch(function() {
    var ta = document.createElement('textarea');
    ta.value = text; document.body.appendChild(ta); ta.select();
    document.execCommand('copy'); document.body.removeChild(ta);
    btn.textContent = '\\u2705 Copied!'; btn.classList.add('copied');
    setTimeout(function() { btn.classList.remove('copied'); }, 1500);
  });
}

function filterCards() {
  var q     = document.getElementById('searchInput').value.toLowerCase();
  var sendF = document.getElementById('sendFilter').value;
  var proofF= document.getElementById('proofFilter').value;

  _rendered = emails.filter(function(e) {
    var matchSend  = !sendF  || (sendF === 'seqflag' ? e.flag === 'seqflag' : e.send === sendF);
    var matchProof = !proofF || e.proof.includes(proofF);
    var matchQ     = !q || e.name.toLowerCase().includes(q)
                       || e.company.toLowerCase().includes(q)
                       || e.subject.toLowerCase().includes(q)
                       || e.body.toLowerCase().includes(q);
    return matchSend && matchProof && matchQ;
  });
  renderCards(_rendered);
}

function clearFilters() {
  document.getElementById('searchInput').value = '';
  document.getElementById('sendFilter').value = '';
  document.getElementById('proofFilter').value = '';
  _rendered = emails.slice();
  renderCards(_rendered);
}

renderCards(emails);
</script>
</body>
</html>'''

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDone! Written {len(html):,} chars to {OUT_PATH}")
