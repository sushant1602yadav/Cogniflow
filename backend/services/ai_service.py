
import json
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:3b",
)

ALLOWED_CATEGORIES = {
    "Delivery",
    "Return",
    "Refund",
    "Payment",
    "Other",
}

ALLOWED_PRIORITIES = {
    "Low",
    "Medium",
    "High",
}

ALLOWED_ACTIONS = {
    "Request Refund",
    "Resolve Ticket",
    "Escalate to Support",
    "Request More Information",
    "No Action",
}


def classify_ticket(issue: str):

    if not issue or not issue.strip():
        raise ValueError("Customer issue cannot be empty.")

    prompt = f"""
You are Cogniflow, an intelligent business support AI.

Analyze this customer complaint:

{issue}

Choose exactly one category:
Delivery, Return, Refund, Payment, Other.

Choose exactly one priority:
Low, Medium, High.

Choose exactly one recommended action:
Request Refund,
Resolve Ticket,
Escalate to Support,
Request More Information,
No Action.

Rules:
- A recommendation is not an authorization.
- Never claim that a refund has been approved.
- Never claim that an action has been executed.
- When information is insufficient, recommend Request More Information.
- When a complaint needs human intervention, recommend Escalate to Support.

Return only valid JSON with these fields:

{{
    "category": "Refund",
    "priority": "High",
    "recommended_action": "Escalate to Support",
    "reason": "Explain the classification and recommendation."
}}
"""

    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/chat",
        json={
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0,
            },
        },
        timeout=120.0,
    )

    response.raise_for_status()

    result = response.json()

    ai_response = result["message"]["content"]

    data = json.loads(ai_response)

    if not isinstance(data, dict):
        raise ValueError("AI returned an invalid response.")

    category = str(
        data.get("category", "")
    ).strip().title()

    priority = str(
        data.get("priority", "")
    ).strip().title()

    recommended_action = str(
        data.get("recommended_action", "")
    ).strip()

    reason = str(
        data.get("reason", "")
    ).strip()

    if category not in ALLOWED_CATEGORIES:
        raise ValueError(
            f"AI returned an unsupported category: {category}"
        )

    if priority not in ALLOWED_PRIORITIES:
        raise ValueError(
            f"AI returned an unsupported priority: {priority}"
        )

    if recommended_action not in ALLOWED_ACTIONS:
        raise ValueError(
            "AI returned an unsupported recommended action."
        )

    if not reason:
        raise ValueError(
            "AI did not provide a classification explanation."
        )

    return {
        "category": category,
        "priority": priority,
        "recommended_action": recommended_action,
        "reason": reason,
    }
