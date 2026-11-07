
from backend.database.db import SessionLocal
from backend.models.audit_log import AuditLog


def audit_log_to_dict(log):
    return {
        "id": log.id,
        "event_type": log.event_type,
        "entity_type": log.entity_type,
        "entity_id": log.entity_id,
        "actor": log.actor,
        "description": log.description,
        "created_at": log.created_at,
    }


def record_audit_event(
    event_type: str,
    entity_type: str,
    entity_id: str,
    actor: str,
    description: str,
):
    db = SessionLocal()

    try:
        event_type = event_type.strip()
        entity_type = entity_type.strip()
        entity_id = str(entity_id).strip()
        actor = actor.strip()
        description = description.strip()

        if not all([
            event_type,
            entity_type,
            entity_id,
            actor,
            description,
        ]):
            raise ValueError(
                "All audit event fields are required."
            )

        log = AuditLog(
            event_type=event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            actor=actor,
            description=description,
        )

        db.add(log)
        db.commit()
        db.refresh(log)

        return audit_log_to_dict(log)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_all_audit_logs(limit: int = 100):
    if limit < 1:
        raise ValueError("Limit must be at least 1.")

    limit = min(limit, 500)

    db = SessionLocal()

    try:
        logs = (
            db.query(AuditLog)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
            .all()
        )

        return [
            audit_log_to_dict(log)
            for log in logs
        ]

    finally:
        db.close()
