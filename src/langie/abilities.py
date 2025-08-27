import re
from typing import Dict, Any
import random

def accept_payload(state: Dict[str, Any]) -> Dict[str, Any]:
    # minimal validation/enrichment
    state_ret = {"intake_done": True}
    return state_ret

def parse_request_text(state: Dict[str, Any]) -> Dict[str, Any]:
    q = state.get("query", "")
    # extract simple intent keywords
    intent = "unknown"
    if "refund" in q.lower() or "return" in q.lower():
        intent = "refund"
    elif "not arrived" in q.lower() or "hasn't arrived" in q.lower() or "haven’t arrived" in q.lower():
        intent = "order_status"
    elif "cancel" in q.lower():
        intent = "cancel_order"
    # try extract order id pattern like #123 or order 123
    m = re.search(r"#?(\d{3,10})", q)
    order_id = m.group(1) if m else None
    return {"parsed_intent": intent, "parsed_order_id": order_id}

def extract_entities(state: Dict[str, Any], server: str="ATLAS") -> Dict[str, Any]:
    # pretend to call external system for entity extraction
    entities = {}
    if state.get("parsed_order_id"):
        entities["order_id"] = state["parsed_order_id"]
    # mock product detection
    if "phone" in state.get("query","").lower():
        entities["product"] = "Smartphone"
    return {"entities": entities, "entities_source": server}

def normalize_fields(state: Dict[str, Any]) -> Dict[str, Any]:
    # normalize priority casing
    p = state.get("priority","Normal")
    return {"priority": p.title()}

def enrich_records(state: Dict[str, Any], server: str="ATLAS") -> Dict[str, Any]:
    # pretend to fetch SLA/ticket history
    ticket_id = state.get("ticket_id")
    history = []
    if ticket_id:
        history = [{"ticket_id": ticket_id, "status": "open", "previous_interactions": 2}]
    sla = {"sla_hours": 48} if state.get("priority","Normal").lower() != "low" else {"sla_hours": 120}
    return {"ticket_history": history, "sla": sla, "enrich_source": server}

def add_flags_calculations(state: Dict[str, Any]) -> Dict[str, Any]:
    # compute simple SLA risk
    priority = state.get("priority","Normal").lower()
    sla_risk = priority == "high"
    return {"sla_risk": sla_risk}

def ask_clarifying_question(state: Dict[str, Any], server: str="ATLAS") -> Dict[str, Any]:
    # if no order id and intent is order_status, ask for order id
    if state.get("parsed_intent") == "order_status" and not state.get("entities", {}).get("order_id"):
        return {"clarify_needed": True, "clarify_question": "Could you share your order number?"}
    return {"clarify_needed": False}

def extract_answer(state: Dict[str, Any], server: str="ATLAS") -> Dict[str, Any]:
    # Assume external actor put the answer into 'customer_response' in state
    ans = state.get("customer_response")
    return {"extracted_answer": ans}

def store_answer(state: Dict[str, Any]) -> Dict[str, Any]:
    # persist customer answer into payload
    if "extracted_answer" in state:
        return {"last_customer_answer": state["extracted_answer"]}
    return {}

def knowledge_base_search(state: Dict[str, Any], server: str="ATLAS") -> Dict[str, Any]:
    # simulate KB search
    intent = state.get("parsed_intent", "unknown")
    if intent == "order_status":
        kb = [{"title":"Order delivery policy", "snippet":"Orders ship in 3-5 business days"}]
    elif intent == "refund":
        kb = [{"title":"Refund policy", "snippet":"Refunds are processed within 7 days"}]
    else:
        kb = [{"title":"General FAQ", "snippet":"Contact support for complex issues"}]
    return {"kb_results": kb}

def store_kb_results(state: Dict[str, Any]) -> Dict[str, Any]:
    return {"kb_stored": True}

def solution_evaluation(state: Dict[str, Any]) -> Dict[str, Any]:
    # Very simple evaluator: if kb has relevant docs and order_id present => high score
    kb = state.get("kb_results", [])
    has_order = bool(state.get("entities", {}).get("order_id"))
    score = 95 if kb and has_order else 75 if kb else 60
    return {"solution_score": score}

def escalation_decision(state: Dict[str, Any], server: str="ATLAS") -> Dict[str, Any]:
    score = state.get("solution_score", 0)
    escalate = score < 90
    # pretend to allocate to human if escalate
    if escalate:
        return {"escalated": True, "escalation_team": "Tier-2"}
    return {"escalated": False}

def update_payload(state: Dict[str, Any]) -> Dict[str, Any]:
    # record decision into payload
    return {"decision_recorded": True}

def update_ticket(state: Dict[str, Any], server: str="ATLAS") -> Dict[str, Any]:
    # escalate → escalated
    if state.get("escalated"):
        return {"ticket_status": "escalated"}
    # high confidence + answer → resolved
    elif state.get("solution_score", 0) >= 90:
        return {"ticket_status": "resolved"}
    return {"ticket_status": "in_progress"}

def close_ticket(state: Dict[str, Any], server: str="ATLAS") -> Dict[str, Any]:
    return {"closed": state.get("ticket_status") == "resolved"}


def generate_customer_response(state: Dict[str, Any]) -> Dict[str, Any]:
    name = state.get("customer_name","Customer")
    if state.get("escalated"):
        text = f"Hi {name}, we've routed this to our specialist team and will get back soon."
    else:
        text = f"Hi {name}, we found a likely answer: {state.get('kb_results',[{}])[0].get('snippet','see details')}."
    return {"response": text}

def execute_api_calls(state: Dict[str, Any], server: str="ATLAS") -> Dict[str, Any]:
    # simulate CRM update
    return {"api_calls_executed": True}

def trigger_notifications(state: Dict[str, Any], server: str="ATLAS") -> Dict[str, Any]:
    return {"notifications_sent": True}

def output_payload(state: Dict[str, Any]) -> Dict[str, Any]:
    # nothing heavy: just mark complete
    return {"complete": True}
