import streamlit as st
import httpx
from backend.services.policy_client import ask_company_policy
from backend.services.agent_client import run_cogniflow_agent
from backend.services.approval_client import (
    get_approval_requests,
    create_approval_request,
    review_approval,
    execute_business_action,
)
from backend.services.audit_client import get_audit_logs

from backend.services.api_client import (
    get_all_tickets,
    update_ticket_status,
    create_ticket,
    classify_customer_ticket,
)


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Cogniflow | Customer Support",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Cogniflow")
st.subheader("Intelligent Customer Support Dashboard")
st.caption("Intelligence That Drives Action.")
st.divider()


# --------------------------------------------------
# FETCH TICKETS FROM FASTAPI
# --------------------------------------------------

try:
    tickets = get_all_tickets()

except httpx.ConnectError:
    st.error(
        "Cannot connect to Cogniflow API. "
        "Please start FastAPI on port 8000."
    )
    st.stop()

except httpx.HTTPStatusError as error:
    st.error(f"API error: {error.response.status_code}")
    st.stop()

except httpx.RequestError as error:
    st.error(f"Network error: {error}")
    st.stop()


# --------------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------------

total = len(tickets)

open_count = sum(
    ticket["status"] == "Open"
    for ticket in tickets
)

pending_count = sum(
    ticket["status"] == "Pending"
    for ticket in tickets
)

resolved_count = sum(
    ticket["status"] == "Resolved"
    for ticket in tickets
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Requests", total)
col2.metric("Open Requests", open_count)
col3.metric("Pending Requests", pending_count)
col4.metric("Resolved Requests", resolved_count)

st.divider()


# --------------------------------------------------
# CUSTOMER SUPPORT REQUESTS
# --------------------------------------------------

st.header("📩 Customer Support Requests")