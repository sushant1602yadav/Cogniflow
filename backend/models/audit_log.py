
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Text,
)

from backend.database.db import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    event_type = Column(
        String,
        nullable=False,
        index=True,
    )

    entity_type = Column(
        String,
        nullable=False,
    )

    entity_id = Column(
        String,
        nullable=False,
        index=True,
    )

    actor = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
