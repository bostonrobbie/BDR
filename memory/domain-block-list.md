# Domain Block List
## Last Updated: 2026-03-19 (Batch 16 session)

Domains where all or most emails bounce. Do NOT enroll contacts at these domains in any Apollo sequence.

## Confirmed Blocks (3+ bounces, pattern confirmed)

| Domain | Company | Bounces | Pattern | Date Confirmed |
|--------|---------|---------|---------|----------------|
| infor.com | Infor | 5/5 | 550 5.4.1 Access denied — domain firewall | 2026-03-17 |
| rsmus.com | RSM US | 5/5 | Address not found | 2026-03-17 |
| checkpoint.com | Check Point Software | 3/3 | Undeliverable (postmaster) | 2026-03-18 |
| kibocommerce.com | Kibo Commerce | 4/4 | Domain-level reject | 2026-03-16 |
| replicon.com | Replicon | 5+ | SMTP 550 hard bounce | 2026-03-16 |
| epicor.com | Epicor | 3/3 | Address not found | 2026-03-18 |
| celonis.de | Celonis | 4 | 550 5.1.1 | 2026-03-14 |
| bungie.net | Bungie | 2/2 | 550 hard bounce | 2026-03-14 |
| draftkings.com | DraftKings | 4 | Address not found | 2026-03-14 |
| ea.com | Electronic Arts | 6 | Domain format invalid | 2026-03-11 |
| fidelity.com | Fidelity | 4+ | Address not found | 2026-03-17 |
| commvault.com | Commvault | 3 | Undeliverable | 2026-03-17 |

## Caution (1-2 bounces, monitor before blocking)

| Domain | Company | Bounces | Note |
|--------|---------|---------|------|
| everbank.com | EverBank | 1 | SPAM blocked (network-level) |
| hims.com | hims & hers | 1/3 | Catchall domain, 1 bounce |
| equiniti.com | Equiniti | 2 | group.internal NDR — monitor |
| mantech-inc.com | ManTech | 2 | Format mismatch (vs mantech.com) |

## Usage Rules
1. Before enrolling ANY new contact, check their email domain against this list
2. If domain is on "Confirmed Blocks" → SKIP, do not enroll
3. If domain is on "Caution" → Enroll with monitoring, verify send within 24 hours
4. When 3+ bounces from same domain → add to Confirmed Blocks
5. This list feeds into the compliance-gate skill pre-enrollment check
