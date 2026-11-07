
import httpx

API_BASE_URL = "http://127.0.0.1:8000"


def get_all_tickets():
    """Fetch all tickets from the Cogniflow API."""

    response = httpx.get(
        f"{API_BASE_URL}/tickets/",
        timeout=10.0,
    )

    response.raise_for_status()

    return response.json()


def get_ticket(ticket_id):
    """Fetch one ticket using its ID."""

    response = httpx.get(
        f"{API_BASE_URL}/tickets/{ticket_id}",
        timeout=10.0,
    )

    response.raise_for_status()

    return response.json()


def update_ticket_status(ticket_id, new_status):
    """Update ticket status through the API."""

    response = httpx.patch(
        f"{API_BASE_URL}/tickets/{ticket_id}/status",
        json={"status": new_status},
        timeout=10.0,
    )

    response.raise_for_status()

    return response.json()

def create_ticket(ticket_data):
    response = httpx.post(
        f"{API_BASE_URL}/tickets/",
        json=ticket_data,
        timeout=10.0,
    )

    response.raise_for_status()
    return response.json()

def classify_customer_ticket(ticket_data):
    response = httpx.post(
        f"{API_BASE_URL}/tickets/classify",
        json=ticket_data,
        timeout=120.0,
    )

    response.raise_for_status()
    return response.json()