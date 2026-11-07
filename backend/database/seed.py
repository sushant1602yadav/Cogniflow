from backend.database.db import SessionLocal, Base, engine
from backend.models.ticket import Ticket

# Create database tables if they do not exist
Base.metadata.create_all(bind=engine)

# Sample customer support tickets
sample_tickets = [
    {
        "ticket_id": "TKT-1001",
        "customer": "Amit Sharma",
        "issue": "My order has been delayed.",
        "category": "Delivery",
        "priority": "High",
        "status": "Open",
        "order_id": "ORD-501",
        "amount": 2499,
    },
    {
        "ticket_id": "TKT-1002",
        "customer": "Priya Verma",
        "issue": "I want to return my product.",
        "category": "Return",
        "priority": "Medium",
        "status": "Pending",
        "order_id": "ORD-502",
        "amount": 1599,
    },
    {
        "ticket_id": "TKT-1003",
        "customer": "Rahul Gupta",
        "issue": "The product I received is damaged.",
        "category": "Refund",
        "priority": "High",
        "status": "Open",
        "order_id": "ORD-503",
        "amount": 3299,
    },
    {
        "ticket_id": "TKT-1004",
        "customer": "Neha Singh",
        "issue": "When will my order arrive?",
        "category": "Delivery",
        "priority": "Low",
        "status": "Resolved",
        "order_id": "ORD-504",
        "amount": 999,
    },
]

db = SessionLocal()

try:
    existing_tickets = db.query(Ticket).count()

    if existing_tickets == 0:
        for ticket_data in sample_tickets:
            db.add(Ticket(**ticket_data))

        db.commit()
        print("Four sample tickets inserted successfully!")
    else:
        print(f"Database already contains {existing_tickets} tickets.")

finally:
    db.close()