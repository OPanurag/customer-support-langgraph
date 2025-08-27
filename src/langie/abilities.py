import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# -------------------------------
# INTAKE
# -------------------------------
def accept_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Accept incoming payload and validate schema."""
    required_fields = ["customer_name", "email", "query", "priority", "ticket_id"]
    missing = [f for f in required_fields if f not in payload]
    if missing:
        logger.warning(f"Missing fields in payload: {missing}")
    return {
        "status": "accepted",
        "missing_fields": missing,
        "payload": payload,
    }


# -------------------------------
# UNDERSTAND
# -------------------------------
def parse_request_text(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Parse the query into structured tokens."""
    query = payload.get("query", "")
    tokens = query.split()
    return {
        "parsed_query": tokens,
        "raw_query": query,
    }


def extract_entities(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Extract entities like product, issue, intent."""
    query = payload.get("query", "").lower()
    entities = {}
    if "refund" in query:
        entities["intent"] = "refund_request"
    if "delay" in query:
        entities["issue"] = "delivery_delay"
    if "invoice" in query:
        entities["product"] = "invoice_service"

    confidence = 0.9 if entities else 0.5
    return {
        "entities": entities,
        "confidence": confidence,
        "missing_entities": not bool(entities),
    }


# -------------------------------
# CLARIFY
# -------------------------------
def ask_clarifying_question(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Ask a clarifying question if confidence is low or entities missing."""
    if payload.get("missing_entities", False):
        question = "Could you please provide more details about the issue?"
    else:
        question = "Can you clarify your request further?"
    return {"clarification_question": question}


def store_customer_answer(payload: Dict[str, Any], answer: str) -> Dict[str, Any]:
    """Store customer's answer for clarification."""
    return {"clarification_answer": answer}


# -------------------------------
# RETRIEVE
# -------------------------------
def store_kb_results(payload: Dict[str, Any], results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Store knowledge base results."""
    return {
        "kb_results": results,
        "kb_hits": len(results),
    }


# -------------------------------
# DECIDE
# -------------------------------
def solution_evaluation(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Evaluate if KB results are sufficient."""
    kb_hits = payload.get("kb_hits", 0)
    if kb_hits > 0:
        decision = "resolve"
    else:
        decision = "escalate"
    return {"decision": decision}


def escalation_decision(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Decide if escalation to human is required."""
    decision = payload.get("decision", "escalate")
    if decision == "escalate":
        reason = "No KB results or low confidence"
    else:
        reason = "Solution found in KB"
    return {"escalation": decision == "escalate", "reason": reason}


# -------------------------------
# ACT
# -------------------------------
def update_ticket(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Update ticket status in system (simulated)."""
    status = "closed" if payload.get("decision") == "resolve" else "escalated"
    return {"ticket_status": status}


def trigger_notifications(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Trigger notifications for stakeholders (simulated)."""
    status = payload.get("ticket_status", "unknown")
    msg = f"Notification sent: Ticket {payload.get('ticket_id')} is {status}."
    logger.info(msg)
    return {"notification": msg}


# -------------------------------
# RESPOND
# -------------------------------
def generate_customer_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Generate final response to the customer."""
    if payload.get("decision") == "resolve":
        response = "We have resolved your issue. Thank you for your patience."
    else:
        response = "Your issue has been escalated to our support team."
    return {"customer_response": response}


# -------------------------------
# COMPLETE
# -------------------------------
def output_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Return final structured output."""
    return {
        "ticket_id": payload.get("ticket_id"),
        "status": payload.get("ticket_status"),
        "response": payload.get("customer_response"),
        "escalation": payload.get("escalation", False),
        "reason": payload.get("reason", ""),
    }
