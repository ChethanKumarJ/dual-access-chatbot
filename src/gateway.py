"""Single chat gateway for both tiers."""
from fastapi import FastAPI, Header
from pydantic import BaseModel
from .retrieval import retrieve_context, audit_log

app = FastAPI(title="dual-access-chatbot")

class ChatRequest(BaseModel):
    query: str
    token: str  # JWT in real version, stubbed for now

def verify_token(token: str) -> dict:
    # TODO: real JWT verification
    # stub: "owner-token" -> owner, anything else -> customer
    if token == "owner-token":
        return {"user_id": "owner-1", "role": "owner"}
    return {"user_id": "anon", "role": "customer"}

@app.post("/chat")
def handle_chat(req: ChatRequest):
    session = verify_token(req.token)
    role = session["role"]

    context = retrieve_context(req.query, role)

    # TODO: call Claude with RAG context
    answer = f"[{role}] stub answer for: {req.query[:100]}"

    # audit if sensitive
    if role == "owner":
        audit_log(session["user_id"], req.query, [c["source"] for c in context])

    return {"answer": answer, "role": role}

@app.get("/health")
def health():
    return {"ok": True}
