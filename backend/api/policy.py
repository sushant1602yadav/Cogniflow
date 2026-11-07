
import httpx

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.services.rag_service import generate_policy_answer


router = APIRouter(
    prefix="/policy",
    tags=["Policy"],
)


class PolicyQuestion(BaseModel):

    question: str = Field(
        min_length=3,
        max_length=2000,
        description="Customer question about company policies",
    )


@router.post("/ask")
def ask_policy(request: PolicyQuestion):

    try:

        result = generate_policy_answer(
            request.question
        )

        return {
            "question": request.question,
            "answer": result["answer"],
            "sources": result["sources"],
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
