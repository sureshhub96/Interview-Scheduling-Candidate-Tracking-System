from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db

from app.dependencies import admin_or_hr

from app.schemas.candidate_schema import CandidateResponse
from app.schemas.interview_schema import InterviewResponse

from app.services.report_service import (
    search_candidates,
    filter_interviews,
    selected_candidates,
    rejected_candidates
)

router = APIRouter()


@router.get(
    "/search",
    response_model=list[CandidateResponse]
)
def search_candidate(
    skill: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_or_hr)
):
    return search_candidates(
        db=db,
        skill=skill,
        page=page,
        limit=limit
    )


@router.get(
    "/interviews",
    response_model=list[InterviewResponse]
)
def interview_report(
    status: str | None = None,
    interviewer_id: int | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_or_hr)
):
    return filter_interviews(
        db=db,
        status=status,
        interviewer_id=interviewer_id,
        page=page,
        limit=limit
    )


@router.get(
    "/selected",
    response_model=list[CandidateResponse]
)
def selected_report(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_or_hr)
):
    return selected_candidates(
        db=db,
        page=page,
        limit=limit
    )


@router.get(
    "/rejected",
    response_model=list[CandidateResponse]
)
def rejected_report(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_or_hr)
):
    return rejected_candidates(
        db=db,
        page=page,
        limit=limit
    )