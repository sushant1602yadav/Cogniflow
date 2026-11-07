
from fastapi import APIRouter, HTTPException, Query

from backend.services.audit_service import get_all_audit_logs

router = APIRouter(
    prefix="/audit",
    tags=["Audit Logs"],
)


@router.get("/")
def get_audit_logs(
    limit: int = Query(default=100, ge=1, le=500),
):
    try:
        logs = get_all_audit_logs(limit=limit)

        return {
            "total": len(logs),
            "logs": logs,
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve audit logs.",
        )
