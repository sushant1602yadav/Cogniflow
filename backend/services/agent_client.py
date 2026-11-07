
import httpx

API_BASE_URL = "http://127.0.0.1:8000"


def run_cogniflow_agent(
    issue: str,
    ticket_id: str | None = None,
):
    if not issue or not issue.strip():
        raise ValueError("Please enter a customer issue.")

    payload = {
        "issue": issue.strip(),
        "ticket_id": ticket_id,
    }

    response = httpx.post(
        f"{API_BASE_URL}/agent/run",
        json=payload,
        timeout=180.0,
    )

    response.raise_for_status()

    return response.json()
