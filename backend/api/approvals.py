
from fastapi import APIRouter, HTTPException, Path
from pydantic import BaseModel, Field

from backend.services.approval_service import (
    create_approval_request,
    get_all_approval_requests,
    review_approval_request,
)


router = APIRouter(
    prefix="/approvals",
    tags=["Human Approvals"],
)


# --------------------------------------------------
# Request schemas
# --------------------------------------------------

class ApprovalCreateRequest(BaseModel):

    ticket_id: str = Field(min_length=1, max_length=50)
    customer: str = Field(min_length=1, max_length=150)
    action_type: str = Field(min_length=1, max_length=100)
    reason: str = Field(min_length=1, max_length=2000)
    amount: float | None = Field(default=None, gt=0)


class ApprovalReviewRequest(BaseModel):

    decision: str = Field(min_length=1, max_length=20)
    reviewed_by: str = Field(min_length=1, max_length=150)
    review_note: str = Field(default="", max_length=2000)


# --------------------------------------------------
# 1. Retrieve all approval requests
# --------------------------------------------------

@router.get("/")
def get_approvals():

    try:
        return get_all_approval_requests()

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve approval requests.",
        )


# --------------------------------------------------
# 2. Create an approval request
# --------------------------------------------------

@router.post("/", status_code=201)
def create_approval(request: ApprovalCreateRequest):

    try:
        result = create_approval_request(
            ticket_id=request.ticket_id.strip(),
            customer=request.customer.strip(),
            action_type=request.action_type.strip(),
            reason=request.reason.strip(),
            amount=request.amount,
        )

        return {
            "message": "Approval request created successfully.",
            "approval": result,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to create approval request.",
        )


# --------------------------------------------------
# 3. Approve or reject a request
# --------------------------------------------------

@router.patch("/{approval_id}/review")
def review_approval(
    approval_id: int = Path(..., ge=1),
    request: ApprovalReviewRequest = ...,
):

    try:
        result = review_approval_request(
            approval_id=approval_id,
            decision=request.decision.strip(),
            reviewed_by=request.reviewed_by.strip(),
            review_note=request.review_note.strip(),
        )

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Approval request not found.",
            )

        return {
            "message": "Approval request reviewed successfully.",
            "approval": result,
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
            detail="Unable to review approval request.",
        )
