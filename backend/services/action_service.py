
from backend.database.db import SessionLocal
from backend.models.approval import Approval
from backend.models.ticket import Ticket
from backend.services.audit_service import record_audit_event


def execute_approved_action(approval_id: int):
    db = SessionLocal()

    try:
        approval = (
            db.query(Approval)
            .filter(Approval.id == approval_id)
            .first()
        )

        if approval is None:
            raise ValueError("Approval request not found.")

        if approval.status != "Approved":
            raise ValueError(
                "This action has not received human approval."
            )

        # --------------------------------------------------
        # 1. Resolve Ticket
        # --------------------------------------------------

        if approval.action_type == "Resolve Ticket":

            ticket = (
                db.query(Ticket)
                .filter(Ticket.ticket_id == approval.ticket_id)
                .first()
            )

            if ticket is None:
                raise ValueError(
                    "Associated ticket not found."
                )

            if ticket.status == "Resolved":

                record_audit_event(
                    event_type="Action Already Completed",
                    entity_type="Action",
                    entity_id=str(approval.id),
                    actor="Cogniflow System",
                    description=(
                        f"Ticket {ticket.ticket_id} was already "
                        f"resolved when action {approval.id} "
                        f"was executed."
                    ),
                )

                return {
                    "success": True,
                    "message": "Ticket is already resolved.",
                    "ticket_id": ticket.ticket_id,
                }

            ticket.status = "Resolved"

            db.commit()

            record_audit_event(
                event_type="Business Action Executed",
                entity_type="Action",
                entity_id=str(approval.id),
                actor="Cogniflow System",
                description=(
                    f"Ticket {ticket.ticket_id} was successfully "
                    f"resolved after approval {approval.id}."
                ),
            )

            return {
                "success": True,
                "message": "Ticket successfully resolved.",
                "ticket_id": ticket.ticket_id,
            }

        # --------------------------------------------------
        # 2. Refund
        # --------------------------------------------------

        elif approval.action_type == "Refund":

            record_audit_event(
                event_type="Business Action Blocked",
                entity_type="Action",
                entity_id=str(approval.id),
                actor="Cogniflow System",
                description=(
                    f"Refund action for ticket "
                    f"{approval.ticket_id} was approved, but "
                    f"automatic payment execution requires "
                    f"a payment gateway integration."
                ),
            )

            return {
                "success": False,
                "message": (
                    "Refund was approved, but automatic payment "
                    "execution requires a payment gateway "
                    "integration. Manual processing is required."
                ),
                "ticket_id": approval.ticket_id,
            }

        # --------------------------------------------------
        # 3. Escalate to Support
        # --------------------------------------------------

        elif approval.action_type == "Escalate to Support":

            record_audit_event(
                event_type="Business Action Requires Integration",
                entity_type="Action",
                entity_id=str(approval.id),
                actor="Cogniflow System",
                description=(
                    f"Escalation for ticket {approval.ticket_id} "
                    f"was approved. A support-team notification "
                    f"or escalation queue integration is required "
                    f"to complete the escalation."
                ),
            )

            return {
                "success": False,
                "message": (
                    "Escalation was approved, but automatic "
                    "support-team routing is not yet integrated. "
                    "Manual escalation is required."
                ),
                "ticket_id": approval.ticket_id,
            }

        # --------------------------------------------------
        # 4. Request More Information
        # --------------------------------------------------

        elif approval.action_type == "Request More Information":

            record_audit_event(
                event_type="Business Action Requires Integration",
                entity_type="Action",
                entity_id=str(approval.id),
                actor="Cogniflow System",
                description=(
                    f"A request for more information concerning "
                    f"ticket {approval.ticket_id} was approved. "
                    f"Customer messaging integration is required "
                    f"to send the request."
                ),
            )

            return {
                "success": False,
                "message": (
                    "The request was approved, but automatic "
                    "customer messaging is not yet integrated. "
                    "Manual customer follow-up is required."
                ),
                "ticket_id": approval.ticket_id,
            }

        # --------------------------------------------------
        # 5. Unsupported action
        # --------------------------------------------------

        else:
            raise ValueError(
                f"Unsupported action type: {approval.action_type}"
            )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
