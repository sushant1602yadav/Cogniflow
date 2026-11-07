
from backend.services.ai_service import classify_ticket
from backend.services.rag_service import generate_policy_answer


def analyze_customer_request(issue: str):
    """
    Analyze a customer request using AI classification
    and retrieval-augmented generation.

    Returns:
        dict: Classification, recommended action,
              policy answer, and supporting sources.
    """

    if not issue or not issue.strip():
        raise ValueError("Customer issue cannot be empty.")

    issue = issue.strip()

    # Step 1: Classify the customer request
    classification = classify_ticket(issue)

    # Step 2: Retrieve the relevant company policy
    policy_result = generate_policy_answer(issue)

    # Step 3: Combine all results
    return {
        "customer_issue": issue,
        "category": classification["category"],
        "priority": classification["priority"],
        "recommended_action": classification["recommended_action"],
        "classification_reason": classification["reason"],
        "policy_answer": policy_result["answer"],
        "policy_sources": policy_result["sources"],
    }
