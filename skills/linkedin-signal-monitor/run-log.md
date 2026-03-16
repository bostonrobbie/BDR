# LinkedIn Signal Monitor — Run Log

### Run 1 — 2026-03-16 07:03 ET (11:03Z)

- **Trigger:** Scheduled (6:05 AM weekday)
- **Profile Views (24h):** — (not captured)
- **InMail Reads (48h):** — (not captured)
- **New Connections:** — (not captured)
- **Signals Appended:** No
- **Errors:** ⚠️ STOPPED — Work Chrome profile not connected to MCP. Chrome MCP was bound to personal "Google Chrome" instance (chrome://newtab/ baseline, LinkedIn navigation timed out). Work Chrome "Robert (testsigma.com) - Chrome" was visible on taskbar but MCP extension not connected to it. Per SKILL.md safety rule: halt execution, alert Rob.
- **Learning Notes:** Scheduled runs require the work Chrome profile to have the MCP extension active and connected. If personal Chrome is open with the extension also installed, MCP may bind to the wrong instance. Rob should ensure the Testsigma Chrome window is the active/primary MCP target before 6:05 AM runs.

---

## Run Record Template

When recording a run, use this format:

```
### Run [N] — [YYYY-MM-DD HH:MM]

- **Trigger:** [scheduled / on-demand]
- **Profile Views (24h):** [N] captured
- **InMail Reads (48h):** [N] captured
- **New Connections:** [N] captured
- **Signals Appended:** [Y/N]
- **Errors:** [None / description]
- **Learning Notes:** [Any insights or anomalies]
```

---
