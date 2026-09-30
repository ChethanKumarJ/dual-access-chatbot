"""Permission-aware retrieval - the whole point of this project."""
# Customer role NEVER touches internal indexes at the code level.
# Not a prompt instruction, just never issues the query.

PUBLIC_INDEXES = ["public-kb"]

INTERNAL_INDEXES = [
    "internal-construction",
    "internal-gov-regs",
    "internal-accounting",
    "internal-paystubs",  # most sensitive, audit-logged
]

def retrieve_context(query: str, role: str) -> list[dict]:
    indexes = list(PUBLIC_INDEXES)
    if role == "owner":
        indexes += INTERNAL_INDEXES
    elif role.startswith("staff_"):
        # e.g. staff_accounts -> accounting + paystubs only
        # TODO: implement sub-role mapping properly
        pass

    # TODO: plug in real vector search
    print(f"[{role}] searching {indexes} for: {query[:50]}")
    return [{"source": idx, "snippet": "TODO"} for idx in indexes]

def audit_log(user_id: str, query: str, docs: list[str]):
    # every paystub/accounting access gets logged with identity
    # TODO: write to Postgres, for now just print
    print(f"AUDIT {user_id}: {query[:80]} -> {docs}")
