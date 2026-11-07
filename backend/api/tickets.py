
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.services.ai_service import classify_ticket
from backend.database.db import get_db
from backend.models.ticket import Ticket
from backend.models.schemas import (
    TicketResponse,
    TicketStatusUpdate,
    TicketCreate,
    TicketClassificationRequest,
)

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


# --------------------------------------------------
# 1. Retrieve all tickets
# --------------------------------------------------

@router.get("/", response_model=list[TicketResponse])
def get_all_tickets(db: Session = Depends(get_db)):

    tickets = db.query(Ticket).all()

    return tickets


# --------------------------------------------------
# 2. Retrieve one ticket
# --------------------------------------------------

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: str,
    db: Session = Depends(get_db),
):

    ticket = (
        db.query(Ticket)
        .filter(Ticket.ticket_id == ticket_id)
        .first()
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    return ticket


# --------------------------------------------------
# 3. Update ticket status
# --------------------------------------------------

@router.patch(
    "/{ticket_id}/status",
    response_model=TicketResponse,
)
def update_ticket_status(
    ticket_id: str,
    update: TicketStatusUpdate,
    db: Session = Depends(get_db),
):

    allowed_statuses = [
        "Open",
        "Pending",
        "Resolved",
    ]

    if update.status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail="Invalid ticket status",
        )

    ticket = (
        db.query(Ticket)
        .filter(Ticket.ticket_id == ticket_id)
        .first()
    )

    if ticket is None:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    ticket.status = update.status

    db.commit()
    db.refresh(ticket)

    return ticket


# --------------------------------------------------
# 4. Create a new ticket
# --------------------------------------------------

@router.post(
    "/",
    response_model=TicketResponse,
    status_code=201,
)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
):

    last_ticket = (
        db.query(Ticket)
        .order_by(Ticket.id.desc())
        .first()
    )

    if last_ticket:
        last_number = int(
            last_ticket.ticket_id.split("-")[1]
        )
        new_number = last_number + 1
    else:
        new_number = 1001

    new_ticket_id = f"TKT-{new_number}"

    new_ticket = Ticket(
        ticket_id=new_ticket_id,
        customer=ticket_data.customer,
        issue=ticket_data.issue,
        category=ticket_data.category,
        priority=ticket_data.priority,
        status="Open",
        order_id=ticket_data.order_id,
        amount=ticket_data.amount,
    )

    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return new_ticket


# --------------------------------------------------
# 5. AI-powered ticket classification
# --------------------------------------------------

@router.post("/classify")
def classify_customer_ticket(
    ticket_data: TicketClassificationRequest,
):

    try:
        result = classify_ticket(ticket_data.issue)

        return {
            "customer": ticket_data.customer,
            "issue": ticket_data.issue,
            "category": result["category"],
            "priority": result["priority"],
            "recommended_action": result["recommended_action"],
            "reason": result["reason"],
            "approval_required": True,
            "message": (
                "This is an AI recommendation only. "
                "Human approval is required before "
                "executing sensitive business actions."
            ),
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="AI classification failed. Please try again.",
        )
