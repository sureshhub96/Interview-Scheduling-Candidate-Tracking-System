from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.candidate_schema import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse
)

from app.services.candidate_service import (
    create_candidate,
    get_candidates,
    get_candidate,
    update_candidate,
    delete_candidate
)

from app.dependencies import (
    admin_or_hr,
    get_current_user
)

router = APIRouter()


@router.post(
    "/",
    response_model=CandidateResponse,
    status_code=201
)
def add_candidate(
    request: CandidateCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_or_hr)
):
    return create_candidate(
        request,
        db
    )


@router.get(
    "/",
    response_model=list[CandidateResponse]
)
def view_candidates(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_or_hr)
):
    return get_candidates(
        db,
        page,
        limit
    )


@router.get(
    "/{candidate_id}",
    response_model=CandidateResponse
)
def view_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_or_hr)
):
    return get_candidate(
        candidate_id,
        db
    )


@router.put(
    "/{candidate_id}",
    response_model=CandidateResponse
)
def edit_candidate(
    candidate_id: int,
    request: CandidateUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return update_candidate(
        candidate_id,
        request,
        db,
        current_user
    )


@router.delete(
    "/{candidate_id}"
)
def remove_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(admin_or_hr)
):
    return delete_candidate(
        candidate_id,
        db
    )