
from sqlalchemy import Column, Integer, String, Text, Float

from backend.database.db import Base


class Ticket(Base):
    """
    Database model for customer support tickets.
    """

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    ticket_id = Column(String(30), unique=True, nullable=False)

    customer = Column(String(100), nullable=False)

    issue = Column(Text, nullable=False)

    category = Column(String(50), nullable=False)

    priority = Column(String(20), nullable=False)

    status = Column(String(20), default="Open", nullable=False)

    order_id = Column(String(30), nullable=False)

    amount = Column(Float, nullable=False)
