from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.models.interview import Interview


def search_candidates(
    db: Session,
    skill: str,
    page: int = 1,
    limit: int = 10
):
    offset = (page - 1) * limit

    return (
        db.query(Candidate)
        .filter(Candidate.skill_set.ilike(f"%{skill}%"))
        .offset(offset)
        .limit(limit)
        .all()
    )


def filter_interviews(
    db: Session,
    status: str = None,
    interviewer_id: int = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(Interview)

    if status:
        query = query.filter(
            Interview.status == status
        )

    if interviewer_id:
        query = query.filter(
            Interview.interviewer_id == interviewer_id
        )

    offset = (page - 1) * limit

    return (
        query.offset(offset)
        .limit(limit)
        .all()
    )


def selected_candidates(
    db: Session,
    page: int = 1,
    limit: int = 10
):
    offset = (page - 1) * limit

    return (
        db.query(Candidate)
        .filter(
            Candidate.application_status == "Selected"
        )
        .offset(offset)
        .limit(limit)
        .all()
    )


def rejected_candidates(
    db: Session,
    page: int = 1,
    limit: int = 10
):
    offset = (page - 1) * limit

    return (
        db.query(Candidate)
        .filter(
            Candidate.application_status == "Rejected"
        )
        .offset(offset)
        .limit(limit)
        .all()
    )