
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
)

from backend.database.db import Base


class Approval(Base):

    __tablename__ = "approvals"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    ticket_id = Column(
        String,
        nullable=False,
        index=True,
    )

    customer = Column(
        String,
        nullable=False,
    )

    action_type = Column(
        String,
        nullable=False,
    )

    amount = Column(
        Float,
        nullable=True,
    )

    reason = Column(
        Text,
        nullable=False,
    )

    status = Column(
        String,
        default="Pending",
        nullable=False,
    )

    requested_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    reviewed_at = Column(
        DateTime,
        nullable=True,
    )

    reviewed_by = Column(
        String,
        nullable=True,
    )

    review_note = Column(
        Text,
        nullable=True,
    )
