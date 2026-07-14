from sqlalchemy.orm import Session
from sqlalchemy import or_

from fastapi import HTTPException, status

from app.models.candidate import Candidate

from app.schemas.candidate_schema import (
    CandidateCreate,
    CandidateUpdate
)


FINAL_STATUS = [
    "Selected",
    "Rejected"
]


def create_candidate(
    request: CandidateCreate,
    db: Session
):

    existing = db.query(Candidate).filter(
        Candidate.email == request.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Candidate email already exists."
        )

    candidate = Candidate(
        name=request.name,
        email=request.email,
        phone=request.phone,
        experience=request.experience,
        skill_set=request.skill_set,
        application_status="Applied"
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


def get_candidates(
    db: Session,
    page: int = 1,
    limit: int = 10
):

    offset = (page - 1) * limit

    candidates = db.query(Candidate)\
        .offset(offset)\
        .limit(limit)\
        .all()

    return candidates


def get_candidate(
    candidate_id: int,
    db: Session
):

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    return candidate


def update_candidate(
    candidate_id: int,
    request: CandidateUpdate,
    db: Session,
    current_user: dict
):

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    # Email uniqueness check
    if request.email:

        existing = db.query(Candidate).filter(
            Candidate.email == request.email,
            Candidate.id != candidate_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already exists."
            )

    # Final status restriction
    if request.application_status in FINAL_STATUS:

        if current_user["role"] not in [
            "HR",
            "Admin"
        ]:
            raise HTTPException(
                status_code=403,
                detail="Only HR/Admin can update final status."
            )

    update_data = request.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(candidate, key, value)

    db.commit()
    db.refresh(candidate)

    return candidate


def delete_candidate(
    candidate_id: int,
    db: Session
):

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    db.delete(candidate)
    db.commit()

    return {
        "message": "Candidate deleted successfully."
    }


def search_candidates(
    skill: str,
    db: Session,
    page: int = 1,
    limit: int = 10
):

    offset = (page - 1) * limit

    return db.query(Candidate).filter(
        Candidate.skill_set.ilike(f"%{skill}%")
    ).offset(offset).limit(limit).all()


def selected_candidates(
    db: Session,
    page: int = 1,
    limit: int = 10
):

    offset = (page - 1) * limit

    return db.query(Candidate).filter(
        Candidate.application_status == "Selected"
    ).offset(offset).limit(limit).all()


def rejected_candidates(
    db: Session,
    page: int = 1,
    limit: int = 10
):

    offset = (page - 1) * limit

    return db.query(Candidate).filter(
        Candidate.application_status == "Rejected"
    ).offset(offset).limit(limit).all()