
from backend.database.db import SessionLocal
from backend.models.ticket import Ticket


def get_customer_order_details(ticket_id: str):

    if not ticket_id or not ticket_id.strip():
        raise ValueError("Ticket ID cannot be empty.")

    db = SessionLocal()

    try:

        ticket = (
            db.query(Ticket)
            .filter(Ticket.ticket_id == ticket_id.strip())
            .first()
        )

        if ticket is None:
            return None

        return {
            "ticket_id": ticket.ticket_id,
            "customer": ticket.customer,
            "issue": ticket.issue,
            "category": ticket.category,
            "priority": ticket.priority,
            "status": ticket.status,
            "order_id": ticket.order_id,
            "amount": ticket.amount,
        }

    finally:
        db.close()
