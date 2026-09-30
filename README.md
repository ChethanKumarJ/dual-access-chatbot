# dual-access-chatbot

One chatbot, two access tiers. Customers get public info, owner login unlocks internal docs (projects, gov regs, accounting, paystubs).

The key decision: enforcement at the retrieval layer, not the prompt. Customer sessions never even query the internal indexes — so there's no prompt-injection path to sensitive data.

## Quick start

```bash
pip install -e .
python -m src.gateway
# POST /chat with {"query": "...", "token": "owner-token"}
```

## How it works

```
login -> JWT with role claim -> chat gateway -> permission-aware retrieval
  customer -> public index only
  owner    -> public + internal (construction, gov, accounting, paystubs)
```

- `src/auth.py` — login, JWT with `role` (stubbed for now)
- `src/retrieval.py` — `retrieve_context(query, role)` only hits allowed indexes
- `src/gateway.py` — single `/chat` endpoint

## RBAC tests

`tests/test_rbac.py` verifies the core invariant: customer sessions can never see internal sources, even for queries like "paystub for john". This is tested at the code level, not just prompt behavior.

## Security notes

- Paystub queries are audit-logged per user (`audit_log`)
- Internal docs encrypted at rest, separate bucket (not implemented here, design only)
- No anonymous Tier 2 — must have credentials
- TODO: real JWT verification, currently stubbed with `owner-token`

## What I'd do next

- [ ] staff sub-roles (e.g. bookkeeper sees accounting but not construction)
- [ ] per-employee paystub scoping
- [ ] plug in real vector DB + Claude RAG
