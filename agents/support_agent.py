
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from backend.services.ai_service import classify_ticket
from backend.services.rag_service import generate_policy_answer
from backend.services.customer_service import get_customer_order_details


class SupportState(TypedDict, total=False):
    issue: str
    ticket_id: str | None

    category: str
    priority: str
    recommended_action: str
    classification_reason: str

    policy_answer: str
    policy_sources: list

    customer_details: dict | None


def classify_request(state: SupportState):

    result = classify_ticket(state["issue"])

    return {
        "category": result["category"],
        "priority": result["priority"],
        "recommended_action": result["recommended_action"],
        "classification_reason": result["reason"],
    }


def retrieve_policy(state: SupportState):

    result = generate_policy_answer(state["issue"])

    return {
        "policy_answer": result["answer"],
        "policy_sources": result["sources"],
    }


def retrieve_customer_details(state: SupportState):

    ticket_id = state.get("ticket_id")

    if not ticket_id:
        return {"customer_details": None}

    details = get_customer_order_details(ticket_id)

    return {
        "customer_details": details,
    }


workflow = StateGraph(SupportState)

workflow.add_node(
    "classify_request",
    classify_request,
)

workflow.add_node(
    "retrieve_policy",
    retrieve_policy,
)

workflow.add_node(
    "retrieve_customer_details",
    retrieve_customer_details,
)

workflow.add_edge(START, "classify_request")

workflow.add_edge(
    "classify_request",
    "retrieve_policy",
)

workflow.add_edge(
    "retrieve_policy",
    "retrieve_customer_details",
)

workflow.add_edge(
    "retrieve_customer_details",
    END,
)

support_agent = workflow.compile()


def run_support_agent(
    issue: str,
    ticket_id: str | None = None,
):

    if not issue or not issue.strip():
        raise ValueError("Customer issue cannot be empty.")

    result = support_agent.invoke(
        {
            "issue": issue.strip(),
            "ticket_id": ticket_id,
        }
    )

    return result
