
import httpx


API_BASE_URL = "http://127.0.0.1:8000"


def ask_company_policy(question: str):

    if not question.strip():
        raise ValueError("Please enter a policy question.")

    response = httpx.post(
        f"{API_BASE_URL}/policy/ask",
        json={
            "question": question,
        },
        timeout=120.0,
    )

    response.raise_for_status()

    return response.json()
