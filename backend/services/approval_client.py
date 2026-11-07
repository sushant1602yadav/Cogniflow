
import httpx

API_BASE_URL = "http://127.0.0.1:8000"


def get_approval_requests():

    response = httpx.get(
        f"{API_BASE_URL}/approvals/",
        timeout=30.0,
    )

    response.raise_for_status()
    return response.json()


def create_approval_request(
    ticket_id: str,
    customer: str,
    action_type: str,
    reason: str,
    amount: float | None = None,
):

    payload = {
        "ticket_id": ticket_id,
        "customer": customer,
        "action_type": action_type,
        "reason": reason,
        "amount": amount,
    }

    response = httpx.post(
        f"{API_BASE_URL}/approvals/",
        json=payload,
        timeout=30.0,
    )

    response.raise_for_status()
    return response.json()


def review_approval(
    approval_id: int,
    decision: str,
    reviewed_by: str,
    review_note: str = "",
):

    payload = {
        "decision": decision,
        "reviewed_by": reviewed_by,
        "review_note": review_note,
    }

    response = httpx.patch(
        f"{API_BASE_URL}/approvals/{approval_id}/review",
        json=payload,
        timeout=30.0,
    )

    response.raise_for_status()
    return response.json()


def execute_business_action(approval_id: int):

    response = httpx.post(
        f"{API_BASE_URL}/actions/{approval_id}/execute",
        timeout=60.0,
    )

    response.raise_for_status()
    return response.json()
