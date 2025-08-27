def call_llm(prompt: str) -> str:
    return f"🤖 Fake LLM says: {prompt}"

def lookup_order(ticket_id: str) -> dict:
    return {"ticket_id": ticket_id, "status": "shipped"}
