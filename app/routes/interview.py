from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.interview_schema import (
    InterviewCreate,
    InterviewUpdate,
    InterviewResponse
)

from app.services.interview_service import (
    create_interview,
    get_interviews,
    get_interview,
    update_interview
)

from app.dependencies import (
    admin_or_hr,
    get_current_user
)

router = APIRouter()


@router.post(
    "/",
    response_model=InterviewResponse,
    status_code=201
)
def schedule_interview(
    request: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_or_hr)
):
    return create_interview(
        request,
        db
    )


@router.get(
    "/",
    response_model=list[InterviewResponse]
)
def view_interviews(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_interviews(
        db,
        current_user
    )


@router.get(
    "/{interview_id}",
    response_model=InterviewResponse
)
def view_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return get_interview(
        interview_id,
        db,
        current_user
    )


@router.put(
    "/{interview_id}",
    response_model=InterviewResponse
)
def edit_interview(
    interview_id: int,
    request: InterviewUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_or_hr)
):
    return update_interview(
        interview_id,
        request,
        db
    )