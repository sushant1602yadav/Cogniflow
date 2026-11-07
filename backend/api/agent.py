
import httpx

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from agents.support_agent import run_support_agent


router = APIRouter(
    prefix="/agent",
    tags=["AI Agent"],
)


class AgentRequest(BaseModel):
    issue: str = Field(
        min_length=3,
        max_length=5000,
        description="Customer support issue",
    )

    ticket_id: str | None = None


@router.post("/run")
def run_agent(request: AgentRequest):

    try:
        result = run_support_agent(
            issue=request.issue,
            ticket_id=request.ticket_id,
        )

        return {
            "message": "Cogniflow AI agent completed the request.",
            "result": result,
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except httpx.HTTPError:
        raise HTTPException(
            status_code=503,
            detail="The AI service is currently unavailable.",
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="The AI agent could not complete the request.",
        )
