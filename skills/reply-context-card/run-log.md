# Reply Context Card — Run Log

_No runs yet._

---

## Log Format

Each run entry:

```
[timestamp] | [contact name] | [company] | [intent] | [priority] | [outcome]
```

Example:
```
2026-03-15 14:35 | Sarah Chen | Spotify | POSITIVE | P0 | → meeting booked 2026-03-18
2026-03-15 15:12 | Marcus Rodriguez | Databricks | SOFT | P1 | → pending reply
```

---

## Fields

- **timestamp:** Date + time card was generated
- **contact name:** Prospect's first + last name
- **company:** Company name
- **intent:** 🟢 POSITIVE / 🟡 SOFT / 🔴 OBJECTION / ⚫ OPT-OUT / ❓ AMBIGUOUS
- **priority:** P0 / P1 / P2 / (none for OPT-OUT)
- **outcome:** Known result (meeting booked, no reply after N days, converted to customer, etc.) — "pending" if still open

