
from datetime import datetime

from backend.database.db import SessionLocal
from backend.models.approval import Approval
from backend.services.audit_service import record_audit_event


def approval_to_dict(approval):
    return {
        "id": approval.id,
        "ticket_id": approval.ticket_id,
        "customer": approval.customer,
        "action_type": approval.action_type,
        "amount": approval.amount,
        "reason": approval.reason,
        "status": approval.status,
        "requested_at": approval.requested_at,
        "reviewed_at": approval.reviewed_at,
        "reviewed_by": approval.reviewed_by,
        "review_note": approval.review_note,
    }


def create_approval_request(
    ticket_id: str,
    customer: str,
    action_type: str,
    reason: str,
    amount: float | None = None,
):
    db = SessionLocal()

    try:
        ticket_id = ticket_id.strip()
        customer = customer.strip()
        action_type = action_type.strip()
        reason = reason.strip()

        if not ticket_id:
            raise ValueError("Ticket ID is required.")

        if not customer:
            raise ValueError("Customer name is required.")

        if not action_type:
            raise ValueError("Action type is required.")

        if not reason:
            raise ValueError("Approval reason is required.")

        if amount is not None and amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        approval = Approval(
            ticket_id=ticket_id,
            customer=customer,
            action_type=action_type,
            amount=amount,
            reason=reason,
            status="Pending",
        )

        db.add(approval)
        db.commit()
        db.refresh(approval)

        result = approval_to_dict(approval)

        record_audit_event(
            event_type="Approval Requested",
            entity_type="Approval",
            entity_id=str(approval.id),
            actor="AI Agent",
            description=(
                f"Approval requested for {approval.action_type} "
                f"on ticket {approval.ticket_id}."
            ),
        )

        return result

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_all_approval_requests():
    db = SessionLocal()

    try:
        approvals = (
            db.query(Approval)
            .order_by(Approval.requested_at.desc())
            .all()
        )

        return [
            approval_to_dict(approval)
            for approval in approvals
        ]

    finally:
        db.close()


def review_approval_request(
    approval_id: int,
    decision: str,
    reviewed_by: str,
    review_note: str = "",
):
    db = SessionLocal()

    try:
        approval = (
            db.query(Approval)
            .filter(Approval.id == approval_id)
            .first()
        )

        if approval is None:
            return None

        decision = decision.strip().title()
        reviewed_by = reviewed_by.strip()
        review_note = review_note.strip()

        if decision not in {"Approved", "Rejected"}:
            raise ValueError(
                "Decision must be either Approved or Rejected."
            )

        if not reviewed_by:
            raise ValueError("Reviewer name is required.")

        if approval.status != "Pending":
            raise ValueError(
                "Only pending approval requests can be reviewed."
            )

        approval.status = decision
        approval.reviewed_by = reviewed_by
        approval.review_note = review_note
        approval.reviewed_at = datetime.utcnow()

        db.commit()
        db.refresh(approval)

        result = approval_to_dict(approval)

        record_audit_event(
            event_type=f"Approval {decision}",
            entity_type="Approval",
            entity_id=str(approval.id),
            actor=reviewed_by,
            description=(
                f"Approval request {approval.id} was "
                f"{decision.lower()} by {reviewed_by}."
            ),
        )

        return result

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
