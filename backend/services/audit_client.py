
import httpx

API_BASE_URL = "http://127.0.0.1:8000"


def get_audit_logs(limit: int = 100):

    response = httpx.get(
        f"{API_BASE_URL}/audit/",
        params={"limit": limit},
        timeout=30.0,
    )

    response.raise_for_status()

    return response.json()
