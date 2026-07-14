from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.feedback_schema import (
    FeedbackCreate,
    FeedbackResponse
)

from app.services.feedback_service import (
    create_feedback,
    get_feedback
)

from app.dependencies import (
    get_current_user
)

router = APIRouter()


@router.post(
    "/",
    response_model=FeedbackResponse,
    status_code=201
)
def add_feedback(
    request: FeedbackCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return create_feedback(
        request,
        db,
        current_user
    )


@router.get(
    "/{interview_id}",
    response_model=FeedbackResponse
)
def view_feedback(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_feedback(
        interview_id,
        db,
        current_user
    )