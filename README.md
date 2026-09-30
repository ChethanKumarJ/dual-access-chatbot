# dual-access-chatbot

One chatbot, two access tiers. Customers get public info, owner login unlocks internal docs (projects, gov regs, accounting, paystubs).

The key decision: enforcement at the retrieval layer, not the prompt. Customer sessions never even query the internal indexes — so there's no prompt-injection path to sensitive data.

## Quick start

```bash
pip install -e .
python -m src.gateway
```

## How it works

```
login -> JWT with role claim -> chat gateway -> permission-aware retrieval
  customer -> public index only
  owner    -> public + internal (construction, gov, accounting, paystubs)
```

- `src/auth.py` — login, JWT with `role`
- `src/retrieval.py` — `retrieve_context(query, role)` only hits allowed indexes
- `src/gateway.py` — single `/chat` endpoint

## Security notes

- Paystub queries are audit-logged per user
- Internal docs encrypted at rest, separate bucket
- No anonymous Tier 2 — must have credentials
