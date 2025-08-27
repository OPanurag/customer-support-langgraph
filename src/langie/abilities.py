import logging
from typing import Dict, Any, List
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# -------------------------------
# INTAKE
# -------------------------------

# def accept_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """Accept incoming payload and validate schema."""
#     required_fields = ["customer_name", "email", "query", "priority", "ticket_id"]
#     missing = [f for f in required_fields if f not in payload]
#     if missing:
#         logger.warning(f"Missing fields in payload: {missing}")
#     return {
#         "status": "accepted",
#         "missing_fields": missing,
#         "payload": payload,
#     }
def accept_payload(state):
    required_fields = ["customer_name", "email", "query", "priority", "ticket_id"]
    for f in required_fields:
        state[f] = state.get(f, "")
    return state



# -------------------------------
# UNDERSTAND
# -------------------------------
# def parse_request_text(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """Parse the query into structured tokens."""
#     query = payload.get("query", "")
#     tokens = query.split()
#     return {
#         "parsed_query": tokens,
#         "raw_query": query,
#     }

def parse_request_text(state):
    text = state["query"]
    order_id = re.search(r"#\d+", text)
    state["entities"] = {"order_id": order_id.group() if order_id else None}
    return state


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

# def extract_entities(state):
#     # Dummy placeholder: in future, integrate spaCy or LLM for intent extraction
#     state["entities"]["intent"] = "order_status"
#     return state


# -------------------------------
# CLARIFY
# -------------------------------
# def ask_clarifying_question(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """Ask a clarifying question if confidence is low or entities missing."""
#     if payload.get("missing_entities", False):
#         question = "Could you please provide more details about the issue?"
#     else:
#         question = "Can you clarify your request further?"
#     return {"clarification_question": question}

def ask_clarifying_question(state):
    entities = state.get("entities", {})
    if not entities.get("order_id"):
        state["clarifying_question"] = "Could you provide your order number?"
    return state



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
# def solution_evaluation(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """Evaluate if KB results are sufficient."""
#     kb_hits = payload.get("kb_hits", 0)
#     if kb_hits > 0:
#         decision = "resolve"
#     else:
#         decision = "escalate"
#     return {"decision": decision}


# def escalation_decision(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """Decide if escalation to human is required."""
#     decision = payload.get("decision", "escalate")
#     if decision == "escalate":
#         reason = "No KB results or low confidence"
#     else:
#         reason = "Solution found in KB"
#     return {"escalation": decision == "escalate", "reason": reason}


def solution_evaluation(state):
    kb_results = state.get("kb_results", [])
    state["ticket_status"] = "resolved" if kb_results else "needs_escalation"
    return state

def escalation_decision(state):
    if state.get("ticket_status") == "needs_escalation":
        state["escalate_to"] = "human_agent"
    return state

# -------------------------------
# ACT
# -------------------------------
# def update_ticket(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """Update ticket status in system (simulated)."""
#     status = "closed" if payload.get("decision") == "resolve" else "escalated"
#     return {"ticket_status": status}


# def trigger_notifications(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """Trigger notifications for stakeholders (simulated)."""
#     status = payload.get("ticket_status", "unknown")
#     msg = f"Notification sent: Ticket {payload.get('ticket_id')} is {status}."
#     logger.info(msg)
#     return {"notification": msg}

def update_ticket(state):
    # Here, save to DB or just simulate for demo
    state["ticket_id"] = state.get("ticket_id") or "TKT-0001"
    return state

def trigger_notifications(state):
    # Could send email/SMS; for demo just log
    print(f"Notify: Ticket {state['ticket_id']} updated for {state['customer_name']}")
    return state



# -------------------------------
# RESPOND
# -------------------------------
# def generate_customer_response(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """Generate final response to the customer."""
#     if payload.get("decision") == "resolve":
#         response = "We have resolved your issue. Thank you for your patience."
#     else:
#         response = "Your issue has been escalated to our support team."
#     return {"customer_response": response}

def generate_customer_response(state):
    kb_results = state.get("kb_results", [])
    if kb_results:
        response = kb_results[0]["answer"]
    else:
        response = "Your query has been forwarded to a support agent."
    state["response"] = response
    return state



# -------------------------------
# COMPLETE
# -------------------------------
# def output_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
#     """Return final structured output."""
#     return {
#         "ticket_id": payload.get("ticket_id"),
#         "status": payload.get("ticket_status"),
#         "response": payload.get("customer_response"),
#         "escalation": payload.get("escalation", False),
#         "reason": payload.get("reason", ""),
#     }

def output_payload(state):
    return state

