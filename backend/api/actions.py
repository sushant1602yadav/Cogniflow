
from fastapi import APIRouter, HTTPException, Path

from backend.services.action_service import (
    execute_approved_action,
)


router = APIRouter(
    prefix="/actions",
    tags=["Business Actions"],
)


@router.post("/{approval_id}/execute")
def execute_action(
    approval_id: int = Path(
        ...,
        ge=1,
        description="ID of the approved business action.",
    )
):

    try:
        result = execute_approved_action(approval_id)

        if not result["success"]:
            raise HTTPException(
                status_code=400,
                detail=result["message"],
            )

        return {
            "success": True,
            "message": "Business action executed successfully.",
            "result": result,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to execute the requested action.",
        )
