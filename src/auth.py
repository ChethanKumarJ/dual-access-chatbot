"""Auth stub - JWT with role claim."""
# TODO: replace with real JWT verification + refresh
def verify_token(token: str) -> dict:
    if token.startswith("owner-"):
        return {"user_id": "owner-1", "role": "owner"}
    if token.startswith("staff-acct"):
        return {"user_id": "staff-1", "role": "staff_accounts"}
    return {"user_id": "anon", "role": "customer"}

def require_owner(session: dict):
    if session.get("role") != "owner":
        raise PermissionError("owner only")
